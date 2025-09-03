import streamlit as st


def auth(username, password) -> bool:
    """
    Simple login function that checks username and password against the database.
    """
    user = st.session_state.db['users'].find_one({'username': username})
    if user and user['password'] == password:
        return True
    return False
