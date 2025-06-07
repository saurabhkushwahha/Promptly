from ai.app import AgentState
from supervisor.supervisor_agent import supervisor_agent
import logging

def process_promptly_ai(query: str, file_path: str = None) -> dict:
    """
    Main entry point for the Promptly assistant.

    Parameters:
    - query (str): The user's input query.
    - file_path (str, optional): Path to a PDF or media file, if relevant.

    Returns:
    - dict: {
        "route": the routed agent name,
        "response": the assistant's answer
      }
    """
    try:
        state: AgentState = {
            "route": "",
            "query": query,
            "file_path": file_path,
            "document_text": None,
            "full_text": None,
            "general_text": None,
        }

        state = supervisor_agent(state)

        if state["route"] == "account_agent":
            from agents.account_agent import account_agent
            state = account_agent(state)

        return {
            "route": state["route"],
            "response": (
                state.get("document_text")
                or state.get("general_text")
                or "Sorry, I couldn't generate a response."
            )
        }

    except Exception as e:
        logging.error(f"[process_promptly_ai] Unexpected error: {e}", exc_info=True)
        return {
            "route": "error",
            "response": "Sorry, something went wrong while processing your request. Please try again later."
        }
