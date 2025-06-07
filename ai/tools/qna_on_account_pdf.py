from langchain.tools import tool
from langchain_core.messages import HumanMessage
from ai.app import llm
import logging

@tool
def ask_questions(full_text: str, user_question: str) -> str:
    """
    Answers a user's question using only the given PDF text (e.g., a bank statement).
    It must not make assumptions, summarize, or fabricate details.
    """

    try:
        prompt = f"""
        You are an intelligent assistant answering questions strictly based on a user's bank statement.

        Here is the extracted text from the bank statement:
        -------------------------
        {full_text}
        -------------------------

        Rules:
        - Only answer based on the data in the statement.
        - Do not summarize, infer, or guess anything.
        - Preserve all numeric values, dates, names, and formats as they appear.
        - If the answer is not explicitly present, respond with:
        "Sorry, the requested information was not found in the statement."

        Now, answer the following question:
        "{user_question}"
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    except Exception as e:
        logging.error(f"[ask_questions] Error during LLM invocation: {e}")
        return "Sorry, there was an error processing your question. Please try again."
