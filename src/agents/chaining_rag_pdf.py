from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
import os

class State (MessagesState):
    customer_name: str
    my_age: int

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.5)

def extractor(state: State):
    new_state: State = {}
    return new_state

def conversation(state: State):
    new_state: State = {}
    if state.get("customer_name", None) is None:
        new_state["customer_name"] = "Joan"
    else:
        new_state["my_age"] = 30

    history = state.get("messages", [])
    last_message = history[-1]
    ai_message = llm.invoke(last_message.content)
    new_state["messages"] = [ai_message]
    return new_state 

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()