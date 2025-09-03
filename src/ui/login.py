import streamlit as st

from core.auth import auth


def login_screen():
    query_params = st.query_params
    prolific_pid = query_params.get("PROLIFIC_PID")
    
    # If user is coming from Prolific, auto-login
    if prolific_pid:
        st.session_state.prolific_pid = prolific_pid
        st.session_state.username = 'prolific'
        st.session_state.logged_in = True
        st.rerun()
    # User is not coming from Prolific, show login form
    else:   
        st.title('Login')
        st.session_state.username = st.text_input('Username')
        st.session_state.password = st.text_input('Password', type='password')

        # If login button is clicked
        if st.button('Login'):
            # Validate credentials
            if auth(st.session_state.username, st.session_state.password):  
                st.session_state.logged_in = True
                st.success('Login successful!')
                st.rerun()
            else:
                st.error('Login details incomplete or wrong.')  
            st.stop()