from src.agents.source_meridian.state import State
import os
import json
import pandas as pd
from typing import Dict, List, Any

def _jsonl_to_df(jsonl_path: str, cap: int = 50) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= cap:
                break
            try:
                rec = json.loads(line)
            except Exception:
                continue

            rows.append({
                "pmid": rec.get("pmid") or rec.get("PMID"),
                "doi": rec.get("doi") or rec.get("DOI"),
                "title": rec.get("title") or rec.get("Title"),
                "abstract": rec.get("abstract") or rec.get("Abstract"),
                "journal": rec.get("journal") or rec.get("Journal"),
                "year": rec.get("year") or rec.get("publication_year") or rec.get("Year"),
                "authors": rec.get("authors"),
                "keywords": rec.get("keywords"),
                "citation_count": rec.get("citation_count"),
                "source": rec.get("source") or "PubMed",
                "url": rec.get("url") or rec.get("link"),
            })
    return pd.DataFrame(rows)


def persist(state: State) -> State:
    """
    Read the JSONL dump, cap to ~50, and persist to CSV at data/raw/pubmed_raw.csv.
    """
    dump_path = state.get("tmp_dump_path", "/Users/joan.estrada/Desktop/platzi-estudios/langraph_agentic_templates/src/agents/source_meridian/data/tmp/pubmed_dump.jsonl")
    csv_out = state.get("csv_out_path") or "/Users/joan.estrada/Desktop/platzi-estudios/langraph_agentic_templates/src/agents/source_meridian/data/raw/pubmed_raw.csv"
    cap = int(state.get("max_records", 50))

    df = _jsonl_to_df(dump_path, cap=cap)

    os.makedirs(os.path.dirname(csv_out), exist_ok=True)
    df.to_csv(csv_out, index=False, encoding="utf-8")

    state["csv_out_path"] = csv_out
    state["pubmed_rows"] = len(df)
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": f"Ingestion complete: {len(df)} rows → {csv_out}"}
    ]
    return state