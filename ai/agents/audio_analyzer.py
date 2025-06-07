from ai.app import AgentState,llm
from ai.tools.audio_processor import extract_text_from_audio
from ai.tools.qna_with_audio import ask_audio_questions
import logging


def audio_analyzer(state:AgentState)-> AgentState:
    """This agent is used to answers any queries related to provide audio file"""

    file_path=state["file_path"]
    audio_full_text=state["audio_full_text"]
    user_query=state["query"]

    try:
        if not file_path and not audio_full_text:
            state["audio_text"] = "Kindly upload a audio file to continue."
            return state

        if file_path and not audio_full_text:
            extracted_text = extract_text_from_audio(file_path)
            if extracted_text:
                state["audio_full_text"] = extracted_text
                state["audio_text"] = "Great! Your audio file is processed! Ask me anything regarding your audio."
            else:
                state["audio_text"] = "Failed to extract audio text. Please try again with a clearer file."
            return state

        if audio_full_text and user_query:
            answer = ask_audio_questions(audio_full_text, user_query)
            state["audio_text"] = answer if answer else "Sorry, I couldn't find that information in your audio."
            return state

    except Exception as e:
        logging.error(f"[audio_analyzer] Error: {e}")
        state["audio_text"] = "Oops! Something went wrong while processing your request. Please try again."

    return state
