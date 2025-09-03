import streamlit as st

from ui.styling import increase_font_size

def completion() -> None:
    """
    Displays the completion code and submission link to the user after they finish the survey.
    Also logs the completion event in the database.
    """
    increase_font_size()
    number_checks_failed = 0
    for manipulation_check in st.session_state.manipulation_checks:
        # Insert each manipulation check into the database
        number_checks_failed += manipulation_check.get('failed')

    st.session_state.db['manipulation_reports'].insert_one({
        'pid': st.session_state.prolific_pid,
        'user_group': st.session_state.username,
        'user_id': st.session_state.user_id,
        'indices': [mc['index'] for mc in st.session_state.manipulation_checks],
        'number_checks': len(st.session_state.manipulation_checks),
        'number_checks_failed': number_checks_failed
    })

    st.success('Evaluation completed! Results sent to MongoDB.')      

    # Stylized completion code box (very dark grey)
    st.markdown(f"""
    <div style="
        padding: 1.5rem; 
        margin: 1.5rem 0; 
        border-radius: 0.5rem; 
        background-color: #1a1a1a; 
        color: white; 
        font-size: 22px; 
        font-weight: bold; 
        text-align: center;
    ">
        {st.secrets.prolific['COMPLETION_CODE']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <p style="margin-bottom: 2rem;">
        Once you've copied the code above, click the link below to return to Prolific and complete your submission:
    </p>
    """, unsafe_allow_html=True)

    # Prolific submission button
    st.markdown(f"""
    <a href="{st.secrets.prolific['URL']}" target="_blank" style="
        display: inline-block;
        font-size: 16px;
        font-weight: 600;
        color: white;
        background-color: transparent;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        text-decoration: none;
        transition: background-color 0.3s ease, color 0.3s ease;
    ">
        Submit on Prolific
    </a>
    """, unsafe_allow_html=True)