from langgraph.graph import StateGraph, START, END, MessagesState
import os, json
from typing import Dict, List, Any
import pandas as pd
from langgraph.graph import StateGraph, START, END, MessagesState
import os, json
from typing import Dict, List, Any
import pandas as pd
from paperscraper.pubmed import get_and_dump_pubmed_papers
from agents.source_meridian.state import State

def _normalize_query(q: Any) -> List[List[str]]:
    """
    paperscraper expects a list of "term-groups", where terms in the same sublist are OR'ed,
    and sublists are AND'ed. E.g., [['diabetes'], ['machine learning', 'deep learning']]
    """
    if q is None:
        # Default: something broad but medical—adjust this later from Agent B or user input
        return [["clinical"], ["machine learning"]]
    if isinstance(q, str):
        return [[q]]
    if isinstance(q, list) and all(isinstance(x, str) for x in q):
        return [q]
    if isinstance(q, list) and all(isinstance(x, list) for x in q):
        return q
    # Fallback
    return [[str(q)]]

def fetch_data(state: State) -> State:
    """
    Retrieve ~50 PubMed records via paperscraper and drop a temporary JSONL dump on disk.
    """
    q = _normalize_query(state.get("pubmed_query", None))
    dump_path = state.get("tmp_dump_path") or "/Users/joan.estrada/Desktop/platzi-estudios/langraph_agentic_templates/src/agents/source_meridian/data/tmp/pubmed_dump.jsonl"
    os.makedirs(os.path.dirname(dump_path), exist_ok=True)
    get_and_dump_pubmed_papers(q, output_filepath=dump_path)

    state["tmp_dump_path"] = dump_path
    return state
