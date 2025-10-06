from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
import os

class State (MessagesState):
    customer_name: str
    my_age: int
    phone: str

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.5)

class ContactInfo(BaseModel):
    """Contact information of a person"""
    name: str = Field(..., description="The full name of the person")
    email: str = Field(..., description="The email address of the person")
    phone: str = Field(..., description="The phone number of the person")
    age: int = Field(..., description="The age of the person", ge=0, le=100)

llm_with_structured_output = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    new_state: State = {}
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    if customer_name is None or len(history) >= 5:
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state

def conversation(state: State):
    new_state: State = {}
    history = state.get("messages", [])
    last_message = history[-1]
    customer_name = state.get("customer_name", "Customer")
    system_message = f"You are a helpful assistant that helps a customer called {customer_name}."
    ai_message = llm.invoke([("system",system_message), ("user",last_message.content)])
    new_state["messages"] = [ai_message]
    return new_state 

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()