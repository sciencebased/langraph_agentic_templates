from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display


class State(TypedDict):
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
        return {
            "my_age": 30
        }
    


builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()