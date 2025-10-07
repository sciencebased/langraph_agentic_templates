from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.conversation.tools import tools
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.5)

def conversation(state: State):
    new_state: State = {}
    history = state.get("messages", [])
    ai_message = llm.invoke([("system", SYSTEM_PROMPT)]+ history) # Only the last message
    new_state["messages"] = [ai_message]
    return new_state