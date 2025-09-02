import streamlit as st

from datetime import datetime

from ui.styling import increase_font_size
from config import QUESTION_SCALE_MAP


def familiarity_check() -> None:
    """
    Display a familiarity check on ML and XAI affinity to the user.
    """
    increase_font_size()
    familiarity_map = QUESTION_SCALE_MAP['familiarity']

    # # Set a default value only if not already set
    # if 'ml_familiarity' not in st.session_state:
    #     st.session_state.ml_familiarity = None

    # Bind radio selection directly to session state
    st.session_state.ml_familiarity = st.radio(
        familiarity_map['ml']['question'],
        familiarity_map['ml']['scale'], 
        index=None,
        horizontal=True
    )
    
    # Add a divider for better separation
    st.divider()
    
    st.session_state.xai_familiarity = st.radio(
        familiarity_map['xai']['question'],
        familiarity_map['xai']['scale'], 
        index=None,
        horizontal=True
    )
    
    # Add a divider for better separation
    st.divider()
    
    st.info("After pressing 'Start Evaluation', please wait a few seconds until random sampling of explanations is completed.")
    
    if st.button('Start Evaluation'):
        if st.session_state.ml_familiarity is not None and st.session_state.xai_familiarity is not None:
            st.session_state.evaluation_started = True
            st.session_state.timestamp = datetime.now().isoformat()
            familiarity = {
                'pid': st.session_state.prolific_pid,
                'user_id': st.session_state.user_id,
                'user_group': st.session_state.username,
                'ml_familiarity': st.session_state.ml_familiarity,
                'xai_familiarity': st.session_state.xai_familiarity,
                'timestamp': st.session_state.timestamp
            }
            st.session_state.db['familiarities'].insert_one(familiarity)
            st.session_state.show_warning = False
            st.rerun()
        else:
            st.session_state.show_warning = True
            
    if st.session_state.show_warning:
        st.warning('Please select an answer before proceeding.')
        
    st.stop()