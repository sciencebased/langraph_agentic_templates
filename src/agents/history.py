from typing import TypedDict
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage
from IPython.display import Image, display


class State(MessagesState):
    customer_name: str
    my_age: int


def node_1(state: State):
    customer_name = state.get("customer_name", None)
    if customer_name is None:
        return {
            "customer_name": "Joan",
            "my_age": 30
        }
    else:
        ai_msg = AIMessage(content= "Hello, how can i help you?")
        return{
            "messages": [ai_msg] + state["messages"]
        }
    


builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()