from langgraph.graph import StateGraph, START, END, MessagesState
from IPython.display import Image, display
from langchain.chat_models import init_chat_model
import random

llm = init_chat_model("anthropic:claude-3-7-sonnet-20250219", temperature=1)

class State(MessagesState):
    customer_name: str
    my_age: int


def node_1(state: State):
    new_state: State = {}
    customer_name = state.get("customer_name", None)
    if customer_name is None:
        new_state["customer_name"] = "Joan"
    else:
        new_state["my_age"] = random.randint(20, 50)

    history = state["messages"]
    ai_message = llm.invoke(history)
    new_state["messages"] = [ai_message]
    print(new_state)
    return new_state


builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()