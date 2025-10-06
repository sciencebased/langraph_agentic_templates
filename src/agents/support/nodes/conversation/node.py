from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.conversation.tools import tools
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.5)
llm_with_tools = llm.bind_tools(tools)

def conversation(state: State):
    new_state: State = {}
    history = state.get("messages", [])
    last_message = history[-1]
    ai_message = llm_with_tools.invoke(last_message.content) # Only the last message
    new_state["messages"] = [ai_message]
    return new_state