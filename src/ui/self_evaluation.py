import streamlit as st

from datetime import datetime, timezone

from config import QUESTION_SCALE_MAP
from ui.styling import increase_font_size, insufficient_answer_warning


def self_evaluation() -> None:
    """
    Displays the self-evaluation questions to the user and stores their responses.
    """
    increase_font_size()
    self_evaluation_map = QUESTION_SCALE_MAP['self_evaluation']

    # Bind radio selection directly to session state
    self_evaluation_response = st.radio(self_evaluation_map['question'],
                                        self_evaluation_map['scale'],
                                        index=None,
                                        horizontal=True)

    # Once submit button to store the response is clicked
    if st.button('Submit Survey'):
        if self_evaluation_response is not None:
            st.session_state.timestamp = datetime.now(timezone.utc).isoformat()
            self_evaluation = {
                'pid': st.session_state.prolific_pid,
                'user_group': st.session_state.username,
                'user_id': st.session_state.user_id,
                'self_evaluation': self_evaluation_response,
                'timestamp': st.session_state.timestamp
            }
            st.session_state.self_evaluation = self_evaluation  # Store in session state for rerun
            st.session_state.db['self_evaluations'].insert_one(self_evaluation)
            st.session_state.show_warning = False
            st.rerun()
        else:
            st.session_state.show_warning = True

    # Display warning if no response is selected
    insufficient_answer_warning()
