import streamlit as st

from datetime import datetime

from ui.briefing import display_briefing
from ui.completion import completion
from ui.evaluation import evaluate_sample
from ui.familiartity import familiarity_check
from ui.login import login_screen
from ui.self_evaluation import self_evaluation

from core.sampling import draw_samples
from core.state import initialize_states

# Initialize streamlit session states
initialize_states()

if not st.session_state.logged_in:
    login_screen()
        
# Show examples before starting evaluation
elif not st.session_state.examples_shown:
    if 'timestamp' not in st.session_state:
        st.session_state.timestamp = datetime.now()
    
    # Display the briefing text to the user
    display_briefing()
    
    # Add a divider for better separation
    st.divider() 
    
    # Once proceeding button to store the response is clicked
    if st.button('Proceed to Survey'):
        st.session_state.examples_shown = True
        st.session_state.db['briefings'].insert_one({
                    'pid': st.session_state.prolific_pid,
                    'user_group': st.session_state.username,
                    'user_id': st.session_state.user_id,
                    'start': st.session_state.timestamp,
                    'end': datetime.now().isoformat()
                })
        st.rerun()
else:
    if not st.session_state.evaluation_started:
        # Ask ML and XAI familiarity questions before starting the evaluation
        familiarity_check()

    # Sample explanations and manipulation checks if not already sampled
    if 'samples' not in st.session_state:
        st.session_state.samples = draw_samples(st.session_state)
    
    if st.session_state.current_index < len(st.session_state.samples):
        # Get the current drawn_sample
        drawn_sample = st.session_state.samples[st.session_state.current_index]
        evaluate_sample(drawn_sample)
        
    elif 'self_evaluation' not in st.session_state:
        self_evaluation()
    else:
        completion()    