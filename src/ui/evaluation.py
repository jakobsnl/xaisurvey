import streamlit as st
import os

from PIL import Image
from datetime import datetime

from config import QUESTION_SCALE_MAP, EXAMPLE_IMAGES, IMAGE_FOLDER
from ui.styling import increase_font_size, insufficient_answer_warning


def visibility_info() -> None:
    """
    Display information about visibility and zooming in the Streamlit app.
    """
    st.info("Consider 'wide mode' in the settings or 'cmd +' / 'ctrl +' to zoom manually for better visibility.")


def display_dummy() -> str | None:
    """
    Display a dummy question to make the page look similar to a proper XAI sample evaluation
    """
    alignment_map = QUESTION_SCALE_MAP['alignment']
    alignment = st.radio(
        alignment_map['question'],
        alignment_map['scale'],
        index=None, 
        key=f'xai_alignment_{st.session_state.current_index}',
        horizontal=True
    )
    return alignment


def display_check(drawn_sample: dict) -> str | None:
    """
    Display the manipulation check question and return the selected answer.
    """
    if drawn_sample.get('type') == 'attention':
        answer = st.radio(
            drawn_sample['question'],
            drawn_sample['scale'],
            index=None,
            key=f"attention_{st.session_state.current_index}",
            horizontal=True
        )
    elif drawn_sample.get('type') == 'attention_note':
        st.markdown(f"**{drawn_sample['note']}**")
        answer = st.radio(
            drawn_sample['question'],
            drawn_sample['scale'],
            index=None,
            key=f'attention_note_{st.session_state.current_index}',
            horizontal=True
        )

    return answer


def evaluate_check(drawn_sample) -> None:
    """
    Run the evaluation process for a given check (attention or attention_note)
    """
    increase_font_size()
    st.markdown(f'### Sample {st.session_state.current_index + 1} of {len(st.session_state.samples)}')
    
    # Add a divider for better separation
    st.divider() 
    
    # Get path of random example image
    explanation_path = EXAMPLE_IMAGES[list(EXAMPLE_IMAGES.keys())[st.session_state.current_index % len(EXAMPLE_IMAGES)]][st.session_state.current_index % 2][0] 
    st.image(Image.open(explanation_path), use_container_width=True)

    # Display info for better visibility
    visibility_info()
    
    # Add a divider for better separation
    st.divider()
    
    # Dummy question to make the page look similar to a proper XAI sample evaluation
    alignment = display_dummy()
    
    # Add a divider for better separation
    st.divider()
    
    # Manipulation check question
    answer = display_check(drawn_sample)
    
    # Once next button to continue the response is clicked
    if st.button('Next'):
        if answer is None or alignment is None:
            st.session_state.show_warning = True
            st.rerun()
        
        manipulation_check = {
            'pid': st.session_state.prolific_pid,
            'user_id': st.session_state.user_id,
            'question': drawn_sample['question'],
            'answer': answer,
            'failed': 0 if answer in drawn_sample.get('correct_answers') else 1,
            'index': st.session_state.current_index,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.db['manipulation_checks'].insert_one(manipulation_check)
        st.session_state.manipulation_checks.append(manipulation_check)
        st.session_state.current_index += 1
        st.session_state.show_warning = False  # Reset warning when user proceeds
        st.rerun()
    
    # Display warning if no response is selected
    insufficient_answer_warning()


def get_alignment() -> str | None:
    """
    Display the alignment question and return the selected answer.
    """
    alignment = None
    alignment_map = QUESTION_SCALE_MAP['alignment']
    alignment = st.radio(
        alignment_map['question'],
        alignment_map['scale'],
        index=None, 
        key=f'xai_alignment_{st.session_state.current_index}',
        horizontal=True
    )
    
    return alignment


def get_relevance() -> str | None:
    """
    Display the relevance question and return the selected answer.
    """
    relevance_map = QUESTION_SCALE_MAP['relevance']
    relevance = st.radio(
        relevance_map['question'],
        relevance_map['scale'],
        index=None, 
        key=f'xai_relevance_{st.session_state.current_index}',
        horizontal=True
    )
    
    return relevance


def evaluate_explanation(drawn_sample: dict) -> None:
    """
    Run the evaluation process for a given XAI explanation sample
    """
    increase_font_size()
    st.markdown(f'### Sample {st.session_state.current_index + 1} of {len(st.session_state.samples)}')
    
    # Add a divider for better separation
    st.divider()
    
    object_folder = drawn_sample['object_folder']
    method = drawn_sample['method']
    threshold = drawn_sample['threshold']
    explanation_path = os.path.join(IMAGE_FOLDER, object_folder, method, threshold)

    # Display the explanation image
    st.image(Image.open(explanation_path), use_container_width=True)
    
    # Display info for better visibility
    visibility_info()

    # Add a divider for better separation
    st.divider() 
    
    # Ask the alignment question and check for a valid response
    alignment = get_alignment()
    
    # Add a divider for better separation
    st.divider() 
    
    # Ask the relevance question and check for a valid response
    relevance = get_relevance()
    
    # Add a divider for better separation
    st.divider()
        
    # Once next button to continue the response is clicked
    if st.button('Next'):
        if alignment is None or relevance is None:
            st.session_state.show_warning = True
            st.rerun()
            
        # Save the responses
        response = {
            'pid': st.session_state.prolific_pid,
            'user_group': st.session_state.username,
            'user_id': st.session_state.user_id,
            'sample': object_folder,
            'method': method,
            'threshold': threshold.split('.')[0],
            'alignment': alignment,
            'relevance': relevance,
            'timestamp': datetime.now().isoformat()
        }

        # Store the response in the database
        st.session_state.db['responses'].insert_one(response)

        # Increase the evaluated drawn_sample from the collection + erase reservation
        st.session_state.db['combinations'].update_one(
            {
                'sample': object_folder,
                'method': method,
                'threshold': threshold
            },
            {
                '$inc': {'times_shown': 1},
                '$set': {'reserved_until': None}
            }
        )
    
        st.session_state.current_index += 1
        st.session_state.current_sample_count += 1
        st.session_state.show_warning = False  # Reset warning when user proceeds
        st.rerun()
        
    # Display warning if no response is selected
    insufficient_answer_warning()

def evaluate_sample(drawn_sample: dict) -> None:
    """
    Run the evaluation process for a given sample
    """
    if drawn_sample.get('type') != 'xai':
        evaluate_check(drawn_sample)
    else:
        evaluate_explanation(drawn_sample)

