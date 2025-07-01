import streamlit as st

def get_max_tokens(length_type):
    if length_type == "long":
        return 800
    elif length_type == "medium":
        return 400
    elif length_type == "short":
        return 100
    else:
        return 300  # default 
    
def check_answer_length_change(current_answer_length):
    """
    Check if the answer length has changed after processing and display appropriate message.
    
    Args:
        current_answer_length (str): The currently selected answer length
    """
    # Initialize processed answer length tracking if not exists
    if "processed_answer_length" not in st.session_state:
        st.session_state.processed_answer_length = None
    
    # Only show messages if PDFs have been processed
    if st.session_state.conversation is not None:
        # Check if answer length has changed after processing
        if (st.session_state.processed_answer_length is not None and 
            st.session_state.processed_answer_length != current_answer_length):
            st.warning("⚠️ Answer length changed! Hit 'Process' again to apply the new setting.")
        else:
            st.info("💡 Hit 'Process' again to refresh my brain!")
    else:
        st.info("💡 Upload PDFs and hit 'Process' to get started!")

def update_processed_answer_length(answer_length):
    """
    Update the processed answer length in session state.
    
    Args:
        answer_length (str): The answer length that was just processed
    """
    st.session_state.processed_answer_length = answer_length
