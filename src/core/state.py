import streamlit as st
import uuid

from collections import Counter

from core.get_database import get_database


def initialize_states():
    """
    Initialize all necessary session state variables for the application.
    This function ensures that each variable is only set if it doesn't already exist,
    preventing overwriting of existing state.
    """
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False 
    if 'prolific_pid' not in st.session_state:
        st.session_state.prolific_pid = None
    if 'evaluation_started' not in st.session_state:
        st.session_state.evaluation_started = False
    if 'examples_shown' not in st.session_state:
        st.session_state.examples_shown = False
    if 'method_count' not in st.session_state:
        st.session_state.method_count = Counter()  # Track how many times each method has been shown
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'current_sample_count' not in st.session_state:
        st.session_state.current_sample_count = 1
    if 'manipulation_checks' not in st.session_state:
        st.session_state.manipulation_checks = []
    if 'ml_familiarity' not in st.session_state:
        st.session_state.ml_familiarity = None
    if 'show_warning' not in st.session_state:
        st.session_state.show_warning = False  # Flag for warning visibility
    if 'db' not in st.session_state:
            st.session_state.db = get_database()
    if 'user_id' not in st.session_state:
            while True:
                user_id = str(uuid.uuid4())  # Generate a new UUID
                if not st.session_state.db['responses'].find_one({'user_id': user_id}):  # Check if the user ID already exists
                    st.session_state.user_id = user_id
                    break   
