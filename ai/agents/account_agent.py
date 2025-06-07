from app import AgentState
from tools.pdf_processor import extract_images_from_pdf
from tools.qna_on_account_pdf import ask_questions
import logging

def account_agent(state: AgentState) -> AgentState:
    """
    Handles account-related queries, especially based on uploaded bank/account PDFs.
    """
    file_path = state.get("file_path")
    full_text = state.get("full_text")
    user_question = state["query"]

    try:
        if not file_path and not full_text:
            state["document_text"] = "Kindly upload a PDF of your account statement to continue."
            return state

        if file_path and not full_text:
            extracted_text = extract_images_from_pdf(file_path)
            if extracted_text:
                state["full_text"] = extracted_text
                state["document_text"] = "Great! Your PDF is processed! Ask me anything about your account statement."
            else:
                state["document_text"] = "Failed to extract PDF text. Please try again with a clearer file."
            return state

        if full_text and user_question:
            answer = ask_questions(full_text, user_question)
            state["document_text"] = answer if answer else "Sorry, I couldn't find that information in your statement."
            return state

    except Exception as e:
        logging.error(f"[account_agent] Error: {e}")
        state["document_text"] = "Oops! Something went wrong while processing your request. Please try again."

    return state
