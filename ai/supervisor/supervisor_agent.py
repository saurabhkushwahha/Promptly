from ai.app import AgentState, safe_invoke
from langchain_core.messages import HumanMessage
import logging

def supervisor_agent(state: AgentState) -> AgentState:
    """
    Routes the user's query to the correct agent or handles general queries directly.
    Promptly is a multi-functional assistant app with various capabilities.
    """

    query = state["query"]
    print(f"Supervisor agent received query: {query}")
    try:
        classification_prompt = f"""
        You are the routing agent for Promptly, a multi-functional assistant app with various capabilities.

        Available specialized agents:
        1. account_agent — Handles queries about bank statements, transactions, balances, and other finance-related documents.
        2. video_analyzer — Handles video-related tasks like summarization or analysis of video content.
        3. audio_analyzer — Handles audio-related tasks such as transcription, summarization, or talking about audio recordings.

        If the user query does NOT clearly belong to any of the above categories, classify it as "general".

        "General" queries include:
        - Small talk and casual conversations
        - Help and app usage questions
        - Fun or chill questions (jokes, trivia, general knowledge)
        - Any other queries not related to accounts, video, or audio

        Respond ONLY with one of these four agent names exactly:
        account_agent, video_analyzer, audio_analyzer, or general

        User query:
        "{query}"
        """

        agent_choice = safe_invoke([HumanMessage(content=classification_prompt)]).strip().lower()
        route_agents = {"account_agent", "video_analyzer", "audio_analyzer"}

        if agent_choice in route_agents:
            state["route"] = agent_choice
        else:
            general_response_prompt = f"""
        You are Promptly's friendly and helpful assistant.

        The user said: "{query}"

        Guidelines:
        - Respond in a friendly, clear, and concise way.
        - For small talk, keep it light and engaging.
        - For help or app questions, clearly explain how Promptly works and its capabilities.
        - For fun or chill queries, respond with relevant, lighthearted replies.
        - Do NOT fabricate document-specific or financial data.
        - Keep answers helpful and on-topic for a multi-functional assistant app.

        Reply to the user now.
        """
            general_response = safe_invoke([HumanMessage(content=general_response_prompt)])
            state["route"] = "supervisor_agent"
            state["general_text"] = general_response

    except Exception as e:
        logging.error(f"Supervisor agent failure: {e}")
        state["route"] = "supervisor_agent"
        state["general_text"] = "Sorry, I had trouble processing your query. Please try again."

    return state
