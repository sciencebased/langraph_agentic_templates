from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
from IPython.display import Image, display
from langchain.chat_models import init_chat_model
import os

load_dotenv()

#When using a RAG from openAI, it is better to send only 
#the last message of the history
#This limitation is not present in more advanced RAGS

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0)
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": [os.getenv("VECTOR_STORE_ID")], # May be an array
}
llm_with_tools = llm.bind_tools([file_search_tool])


class State(MessagesState):
    customer_name: str
    my_age: int


def node_1(state: State):
    new_state: State = {}
    customer_name = state.get("customer_name", None)
    if customer_name is None:
        new_state["customer_name"] = "Joan"
    else:
        new_state["my_age"] = 30
    history = state.get("messages", [])
    last_message = history[-1]
    ai_message = llm_with_tools.invoke(last_message.content) # Only the last message
    new_state["messages"] = [ai_message]
    return new_state

builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()