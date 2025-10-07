from langgraph.graph import StateGraph, START, END, MessagesState


from agents.support.state import State

from agents.source_meridian.nodes.fetch_data.node import fetch_data
from agents.source_meridian.nodes.classifier.node import classify_specialty_node as classifier
from agents.source_meridian.nodes.extract.node import extract
from agents.source_meridian.nodes.persist.node import persist


builder = StateGraph(State)
builder.add_node("fetch_data", fetch_data)
builder.add_node("extract", extract)
builder.add_node("persist", persist)
builder.add_node("classifier", classifier)

builder.add_edge(START, 'fetch_data')
builder.add_edge('fetch_data', 'extract')
builder.add_edge('extract', 'persist')
builder.add_edge('persist', 'classifier')
builder.add_edge('classifier', END)

agent = builder.compile()