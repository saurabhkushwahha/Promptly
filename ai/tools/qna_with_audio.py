from app import llm
from langchain.tools import tool
import logging

@tool
def ask_audio_questions(audio_full_text: str, question: str) -> str:
    """
    Stub function to simulate answering questions from audio transcription.
    Replace with your own logic or LLM prompt if needed.
    """
    prompt = f"""
    You are an assistant answering questions based on the following audio transcript:

    ----------------
    {audio_full_text}
    ----------------

    User question: "{question}"

    Rules:
    - Only answer based on the transcript above.
    - Do not make up or guess anything.
    - If the answer isn't explicitly in the transcript, respond:
      "Sorry, I couldn't find that information in your audio."

    Answer:
    """
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        logging.error(f"[ask_audio_questions] Error: {e}")
        return "Sorry, an error occurred while trying to answer your question."