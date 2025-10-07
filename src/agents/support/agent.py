from langgraph.graph import StateGraph, START, END, MessagesState


from agents.support.state import State
from agents.support.nodes.extractor.node import extractor
from agents.support.nodes.conversation.node import conversation
from agents.support.nodes.relevant_questions.agent import agent as relevant_questions
from agents.support.routes.intent.route import intent_route

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)
builder.add_node("relevant_questions", relevant_questions)

builder.add_edge(START, 'extractor')
builder.add_conditional_edges('extractor', intent_route)
builder.add_edge('conversation', END)
builder.add_edge('relevant_questions', END)

agent = builder.compile()