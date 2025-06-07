import logging
from graph_builder import graph

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def run_promptly(query: str, file_path: str = None):
    logger.info(f"Received query: {query} | file_path: {file_path}")

    state = {
        "route": "",
        "query": query,
        "file_path": file_path,
        "document_text": None,
        "full_text": None,
        "general_text": None,
        "audio_full_text": None,
        "audio_text": None
    }

    try:
        final_state = graph.invoke(state)
        logger.info(f"Final route: {final_state['route']}")
    except Exception as e:
        logger.error(f"Error invoking graph: {e}", exc_info=True)
        return {
            "route": "error",
            "response": "An internal error occurred while processing your request."
        }

    response = (
        final_state.get("document_text")
        or final_state.get("audio_text")
        or final_state.get("general_text")
        or "Sorry, I couldn't generate a response."
    )
    logger.info(f"Response: {response}")

    return {
        "route": final_state["route"],
        "response": response
    }
