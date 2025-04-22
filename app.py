import datetime
import json
import os
import random
import streamlit as st

from PIL import Image
from pymongo import MongoClient

from config import IMAGE_FOLDER, RESULTS_FILE, NUM_SAMPLES, QUESTION_SCALE_MAP, EXAMPLE_IMAGES
from get_database import get_database
from datetime import datetime
    
    
# Function to randomly pick an explanation method and threshold image
def sample_explanation(object_folder: str) -> tuple:
    explanations_path = os.path.join(IMAGE_FOLDER, object_folder)
    if not os.path.exists(explanations_path):
        return None, None
    
    methods = [m for m in os.listdir(explanations_path) if os.path.isdir(os.path.join(explanations_path, m))]
    if not methods:
        return None, None
    
    selected_method = random.choice(methods)
    method_path = os.path.join(explanations_path, selected_method)
    
    thresholds = [t for t in os.listdir(method_path) if t.endswith(('.png', '.jpg', '.jpeg'))]
    if not thresholds:
        return selected_method, None
    
    selected_threshold = random.choice(thresholds)
    return selected_method, selected_threshold

db = get_database()
collection = db['responses']

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
if 'sampled_objects' not in st.session_state:
    object_folders = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isdir(os.path.join(IMAGE_FOLDER, f))]
    st.session_state.sampled_objects = random.sample(object_folders, min(NUM_SAMPLES, len(object_folders)))
if 'sampled_explanations' not in st.session_state:
    st.session_state.sampled_explanations = [sample_explanation(obj) for obj in st.session_state.sampled_objects]
if 'show_warning' not in st.session_state:
    st.session_state.show_warning = False  # Flag for warning visibility

# Show examples before starting evaluation
if not st.session_state.examples_shown:
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
        index=None
    )

    if st.button('Start Evaluation'):
        if selected_familiarity is not None:
            st.session_state.evaluation_started = True
            st.session_state.ml_familiarity = selected_familiarity  # Save only if valid
            st.rerun()
        else:
            st.warning('Please select an answer before proceeding.')

else:
    # Display images and questions
    if st.session_state.current_index < len(st.session_state.sampled_objects):
        # Persist the warning message
        object_folder = st.session_state.sampled_objects[st.session_state.current_index]
        method, threshold_image = st.session_state.sampled_explanations[st.session_state.current_index]
        
        if method is None or threshold_image is None:
            st.warning('No valid explanation found for this object. Skipping...')
            st.session_state.current_index += 1
            st.rerun()
        else:
            explanation_path = os.path.join(IMAGE_FOLDER, object_folder, method, threshold_image)
            
            st.image(Image.open(explanation_path), use_container_width=True)

            # Ask the alignment question and check for a valid response
            alignment = None
            alignment_map = QUESTION_SCALE_MAP['alignment']
            alignment = st.radio(
                alignment_map['question'],
                alignment_map['scale'],
                index=None, 
                key=f'xai_alignment_{st.session_state.current_index}'  # Unique key
            )
            # Ask the relevance question and check for a valid response
            relevance = None
            relevance_map = QUESTION_SCALE_MAP['relevance']
            relevance = st.radio(
                relevance_map['question'],
                relevance_map['scale'],
                index=None, 
                key=f'xai_relevance_{st.session_state.current_index}'
            )
            
            # Display warning if no response is selected
            if st.session_state.show_warning:
                st.warning('Please select answers to continue.')
                
            if st.button('Next'):
                if alignment is None or relevance is None:
                    st.session_state.show_warning = True
                    st.rerun()
                # Save the responses
                st.session_state.responses.append({
                    'object_folder': object_folder,
                    'method': method,
                    'threshold_image': threshold_image.split('.')[0],
                    'alignment': alignment,
                    'relevance': relevance
                })
                st.session_state.current_index += 1
                st.session_state.show_warning = False  # Reset warning when user proceeds
                st.rerun()
    else:
        # Save results to MongoDB
        results = {
            'ml_familiarity': st.session_state.ml_familiarity,
            'responses': st.session_state.responses,
            'timestamp': datetime.now().isoformat()
        }
        collection.insert_one(results)
        st.success('Evaluation completed! Results sent to MongoDB.')
