from app import llm
from langchain.tools import tool
import whisper
import logging
import os

@tool
def extract_text_from_audio(file_path: str) -> str:
    """
    This tool extracts transcribed text from an audio file using OpenAI's Whisper model.
    """

    try:
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return f"Error: File '{file_path}' not found."

        logging.info(f"Loading Whisper model...")
        model = whisper.load_model("base")

        logging.info(f"Transcribing audio file: {file_path}")
        result = model.transcribe(file_path)

        return result.get("text", "No transcribed text found.")

    except Exception as e:
        logging.exception("Audio transcription failed.")
        return f"An error occurred while transcribing the audio: {str(e)}"
