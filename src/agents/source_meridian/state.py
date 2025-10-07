
from langgraph.graph import StateGraph, START, END, MessagesState
from typing import List, Dict, Any

class State(MessagesState):
    customer_name: str
    my_age: int
    pubmed_data: List[Dict[str, Any]] = None
    pubmed_query: str = "cancer"
    csv_path: str = "data/raw/pubmed_raw.csv"
    csv_out_path: str = "data/processed/pubmed_processed.csv"