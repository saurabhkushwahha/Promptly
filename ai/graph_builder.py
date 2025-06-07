import logging
from langgraph.graph import StateGraph
from app import AgentState
from supervisor.supervisor_agent import supervisor_agent
from agents.account_agent import account_agent
from agents.audio_analyzer import audio_analyzer

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def router_node(state: AgentState) -> AgentState:
    logger.info(f"Routing query: {state.get('query')}")
    try:
        new_state = supervisor_agent(state)
        logger.info(f"Route decided: {new_state['route']}")
        return new_state
    except Exception as e:
        logger.error(f"Error in supervisor_agent: {e}", exc_info=True)
        state["route"] = "supervisor_agent"
        state["general_text"] = "Oops, something went wrong in routing. Please try again."
        return state

def account_node(state: AgentState) -> AgentState:
    logger.info("Processing with account_agent")
    try:
        return account_agent(state)
    except Exception as e:
        logger.error(f"Error in account_agent: {e}", exc_info=True)
        state["document_text"] = "An error occurred while processing your account request."
        return state

def audio_node(state: AgentState) -> AgentState:
    logger.info("Processing with audio_analyzer")
    try:
        return audio_analyzer(state)
    except Exception as e:
        logger.error(f"Error in audio_analyzer: {e}", exc_info=True)
        state["audio_text"] = "An error occurred while processing your audio request."
        return state

def general_node(state: AgentState) -> AgentState:
    logger.info("Processing general query in supervisor_agent")
    return state

builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("account_agent", account_node)
builder.add_node("audio_analyzer", audio_node)
builder.add_node("general", general_node)

builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "account_agent": "account_agent",
        "audio_analyzer": "audio_analyzer",
        "supervisor_agent": "general"
    }
)

builder.set_finish_point("account_agent")
builder.set_finish_point("audio_analyzer")
builder.set_finish_point("general")

graph = builder.compile()
logger.info("StateGraph compiled successfully.")
