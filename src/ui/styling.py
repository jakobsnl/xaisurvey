import streamlit as st


def increase_font_size() -> None:
    """
    Increases the font size of radio titles in the Streamlit app.
    """
    st.markdown("""
            <style>
            div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
            font-size: 18px;
            }
            </style>
            """,
                unsafe_allow_html=True)


def insufficient_answer_warning() -> None:
    """
    Displays a warning message if the user tries to submit without selecting an answer.
    """
    if st.session_state.show_warning:
        st.warning('Please select an answer to continue.')
