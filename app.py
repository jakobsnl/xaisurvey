import datetime
import json
import os
import random
import streamlit as st
import uuid

from PIL import Image
from datetime import datetime

from config import IMAGE_FOLDER, NUM_SAMPLES, QUESTION_SCALE_MAP, EXAMPLE_IMAGES
from get_database import get_database
from permuation import populate_samples


# Login function
def login(username, password):
    user = users_collection.find_one({"username": username})
    if user and user['password']==password:
        return True
    return False


def draw_samples(num_samples, remaining_samples):
    """
    samples unique object folders and selects one method and threshold image for each.
    Ensures that folders with no remaining drawn_samples are skipped.
    Repopulates the collection if all drawn_samples are exhausted.
    """
    drawn_samples = []

    while len(drawn_samples) < num_samples:
        # Check if there are any unused drawn_samples
        if remaining_samples.count_documents({}) == 0:
            # If no drawn_samples are left, repopulate the collection
            populate_samples()

        # Get all unique object folders with remaining drawn_samples
        unique_folders = remaining_samples.distinct('sample')

        # Filter out folders that have no remaining drawn_samples
        valid_folders = [
            folder for folder in unique_folders
            if remaining_samples.count_documents({'sample': folder}) > 0
        ]

        # If there are no valid folders left after repopulation, break the loop
        if not valid_folders:
            print("No valid folders left to sample from, even after repopulation.")
            break

        # Randomly select up to the remaining required remaining_samples from valid folders
        remaining_num_samples = num_samples - len(drawn_samples)
        sampled_folders = random.sample(valid_folders, min(remaining_num_samples, len(valid_folders)))

        # For each folder, randomly select one method and threshold image
        for folder in sampled_folders:
            # Get all methods for the folder
            methods = remaining_samples.distinct('method', {'sample': folder})

            # Randomly select a method
            selected_method = random.choice(methods)

            # Get all thresholds for the selected folder and method
            thresholds = remaining_samples.distinct('threshold', {'sample': folder, 'method': selected_method})

            # Randomly select a threshold
            selected_threshold = random.choice(thresholds)

            # Find the specific drawn_sample and mark it as reserved
            drawn_sample = remaining_samples.find_one_and_update(
                {'sample': folder, 'method': selected_method, 'threshold': selected_threshold, 'reserved': {'$ne': True}},
                {'$set': {'reserved': True}},  # Mark as reserved
                sort=[('_id', 1)],  # Sort to ensure deterministic order
                return_document=True  # Return the updated document
            )
            if drawn_sample:
                drawn_samples.append(drawn_sample)

    return drawn_samples


db = get_database()
users_collection = db['users']
remaining_samples = db['combinations']
familiarities = db['familiarities']
responses = db['responses']

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
# Generate a unique user ID when the survey starts
if 'user_id' not in st.session_state:
    while True:
        user_id = str(uuid.uuid4())  # Generate a new UUID
        if not responses.find_one({'user_id': user_id}):  # Check if the user ID already exists
            st.session_state.user_id = user_id
            break
        
# Update session state initialization
if 'sampled_explanations' not in st.session_state:
    st.session_state.sampled_explanations = []
    drawn_samples = draw_samples(NUM_SAMPLES, remaining_samples)
    for drawn_sample in drawn_samples:
        sample_folder = drawn_sample['sample']
        method = drawn_sample['method']
        threshold = drawn_sample['threshold']
        st.session_state.sampled_explanations.append({
            'object_folder': sample_folder,
            'method': method,
            'threshold': threshold
        })
        print(f"Sampled: {sample_folder}, {method}, {threshold}")

# Initialize session state variables
if 'evaluation_started' not in st.session_state:
    st.session_state.evaluation_started = False
if 'examples_shown' not in st.session_state:
    st.session_state.examples_shown = False
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'ml_familiarity' not in st.session_state:
    st.session_state.ml_familiarity = None
if 'show_warning' not in st.session_state:
    st.session_state.show_warning = False  # Flag for warning visibility

if not st.session_state.logged_in:
    st.title("Login")  # Login UI
    st.session_state.username = st.text_input("Username")
    st.session_state.password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(st.session_state.username, st.session_state.password):  # Validate credentials
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")  # Error message for invalid credentials
        st.stop()
        
# Show examples before starting evaluation
elif not st.session_state.examples_shown:
    # Display scale at the top with intuitive descriptions
    st.subheader('Explanation Alignment Scale')
    st.write('You will be asked to rank explanations based on the alignment with the ground truth. The scale ranges from 1 (poor explanation) to 5 (perfect explanation).')
    st.write("""
    - **1 - Not at all**: The explanation does not align with the ground truth at all. There is no relevance between the highlighted regions and the key features of the object.
    - **2**: The explanation is partially aligned, but it misses significant aspects of the object. The explanation highlights some relevant areas, but overall it's not very clear.
    - **3**: The explanation is somewhat aligned, but not perfectly. It touches on key areas, but there are still significant areas of improvement.
    - **4**: The explanation is mostly aligned, but there may be small parts that are not clearly relevant. It supports the object classification well, but there is room for slight improvement.
    - **5 - Perfectly aligned**: The explanation is perfectly aligned with the ground truth. The highlighted areas clearly correspond to the most important features of the object, making it easy to understand why the model made its decision.
    """)
    
    st.subheader('Example Evaluations')
    st.write('Below are two example cases to help you understand how to rank explanations.')
    
    # Display the examples
    for exp_path, rank in EXAMPLE_IMAGES:
        st.image(Image.open(exp_path), caption=f'Explanation', use_container_width=True)
        st.write(f'This should be ranked as [{rank}] out of 5.')
        
        # Dummy Intuition on why to rank like this
        if rank == 1:
            st.write("Intuition: This explanation is considered poor because it does not align well with the ground truth. The highlighted regions in the explanation don't provide enough insight into the relevant parts of the image. It's not clear how the explanation supports the object classification.")
        elif rank == 5:
            st.write("Intuition: This explanation is highly aligned with the ground truth. It correctly highlights the key features that are most important for the classification, making it easy to understand why the model made its decision.")
    
    if st.button('Proceed to Survey'):
        st.session_state.examples_shown = True
        st.rerun()

# Initial question
elif not st.session_state.evaluation_started:
    familiarity_map = QUESTION_SCALE_MAP['familarity']
    
    # Set a default value only if not already set
    if 'ml_familiarity' not in st.session_state:
        st.session_state.ml_familiarity = None

    # Bind radio selection directly to session state
    selected_familiarity = st.radio(
        familiarity_map['question'],
        familiarity_map['scale'], 
        index=None,
        horizontal=True
    )

    if st.button('Start Evaluation'):
        if selected_familiarity is not None:
            st.session_state.evaluation_started = True
            st.session_state.ml_familiarity = selected_familiarity
            st.session_state.timestamp = datetime.now().isoformat()
            familiarity = {
                'user_group': st.session_state.username,
                'user_id': st.session_state.user_id,
                'ml_familiarity': st.session_state.ml_familiarity,
                'timestamp': st.session_state.timestamp
            }
            familiarities.insert_one(familiarity)
            st.rerun()
        else:
            st.warning('Please select an answer before proceeding.')

else:
    # Display images and questions
    if st.session_state.current_index < len(st.session_state.sampled_explanations):
        # Get the current drawn_sample
        drawn_sample = st.session_state.sampled_explanations[st.session_state.current_index]
        object_folder = drawn_sample['object_folder']
        method = drawn_sample['method']
        threshold = drawn_sample['threshold']

        explanation_path = os.path.join(IMAGE_FOLDER, object_folder, method, threshold)
        st.image(Image.open(explanation_path), use_container_width=True)

        # Ask the alignment question and check for a valid response
        alignment = None
        alignment_map = QUESTION_SCALE_MAP['alignment']
        alignment = st.radio(
            alignment_map['question'],
            alignment_map['scale'],
            index=None, 
            key=f'xai_alignment_{st.session_state.current_index}',
            horizontal=True
        )
        # Ask the relevance question and check for a valid response
        relevance = None
        relevance_map = QUESTION_SCALE_MAP['relevance']
        relevance = st.radio(
            relevance_map['question'],
            relevance_map['scale'],
            index=None, 
            key=f'xai_relevance_{st.session_state.current_index}',
            horizontal=True
        )
        
        # Display warning if no response is selected
        if st.session_state.show_warning:
            st.warning('Please select answers to continue.')
            
        if st.button('Next'):
            if alignment is None or relevance is None:
                st.session_state.show_warning = True
                st.rerun()
            # Save the responses
            response = {
                'user_group': st.session_state.username,
                'user_id': st.session_state.user_id,
                'sample': object_folder,
                'method': method,
                'threshold': threshold.split('.')[0],
                'alignment': alignment,
                'relevance': relevance,
                'timestamp': datetime.now().isoformat()
            }

            responses.insert_one(response)

            # Delete the evaluated drawn_sample from the collection
            remaining_samples.delete_one({
                'sample': object_folder,
                'method': method,
                'threshold': threshold
            })
            
            st.session_state.current_index += 1
            st.session_state.show_warning = False  # Reset warning when user proceeds
            st.rerun()
    else:
        st.success('Evaluation completed! Results sent to MongoDB.')