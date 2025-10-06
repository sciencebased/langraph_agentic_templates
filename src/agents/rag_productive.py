from langgraph.graph import StateGraph, START, END, MessagesState


from agents.support.state import State
from agents.support.nodes.extractor.node import extractor
from agents.support.nodes.conversation.node import conversation

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()

#### MOVED TO support/agent.py