from typing import TypedDict, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("promptly.log"),
        logging.StreamHandler()
    ]
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="mistral-saba-24b",
        temperature=0.3,
        verbose=False
    )
except Exception as e:
    logging.critical(f"Failed to initialize LLM: {e}")
    raise RuntimeError("LLM initialization failed. Check your API key and environment setup.")

class AgentState(TypedDict):
    route: str
    query: str
    file_path: Optional[str]
    document_text: Optional[str]
    full_text: Optional[str]
    general_text: Optional[str]
    audio_full_text:Optional[str]
    audio_text:Optional[str]

def safe_invoke(prompt: HumanMessage) -> str:
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        logging.error(f"LLM invocation failed: {e}")
        return "Sorry, an internal error occurred while processing your request."
