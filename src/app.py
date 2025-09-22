import streamlit as st

from datetime import datetime, timezone

from ui.briefing import display_briefing, store_briefing
from ui.completion import completion
from ui.evaluation import evaluate_sample
from ui.familiartity import familiarity_check
from ui.login import login
from ui.self_evaluation import self_evaluation
from core.sampling import draw_samples
from core.state import initialize_states

# Initialize streamlit session states to store user progress and data
initialize_states()

# User verification if not logged in
if not st.session_state.logged_in:
    login()

# Show examples before starting evaluation
elif not st.session_state.examples_shown:
    if 'timestamp' not in st.session_state:
        st.session_state.timestamp = datetime.now(timezone.utc).isoformat()

    # Display the briefing text to the user
    display_briefing()

    # Add a divider for better separation
    st.divider()

    # Once proceeding button to store the response is clicked
    if st.button('Proceed to Survey'):
        # Write briefing stats to DB and set examples_shown to True
        store_briefing()
else:
    # Ask ML and XAI familiarity questions before starting the evaluation
    if not st.session_state.evaluation_started:
        familiarity_check()

    # Sample explanations and manipulation checks if not already sampled
    if 'samples' not in st.session_state:
        st.session_state.samples = draw_samples()

    # Get the current drawn_sample
    if st.session_state.current_index < len(st.session_state.samples):
        drawn_sample = st.session_state.samples[st.session_state.current_index]
        evaluate_sample(drawn_sample)

    elif 'self_evaluation' not in st.session_state:
        self_evaluation()
    else:
        completion()
