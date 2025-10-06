
from langgraph.graph import StateGraph, START, END, MessagesState

class State (MessagesState):
    customer_name: str
    my_age: int
    phone: str