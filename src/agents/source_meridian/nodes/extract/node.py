import os, csv, io, ast
from typing import Any, Dict, List, Optional
from src.agents.source_meridian.state import State

# ---------- helpers ----------
def _parse_list_field(raw: Optional[str]) -> List[str]:
    if not raw or not raw.strip():
        return []
    s = raw.strip()
    try:
        val = ast.literal_eval(s)
        if isinstance(val, (list, tuple)):
            return [str(x).strip() for x in val if str(x).strip()]
    except Exception:
        pass
    parts = [p.strip() for p in s.split(",") if p.strip()]
    seen, out = set(), []
    for p in parts:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out

def _parse_int(raw: Optional[str]) -> Optional[int]:
    if not raw:
        return None
    try:
        return int(raw)
    except Exception:
        try:
            return int(float(raw))
        except Exception:
            return None

def csv_to_table_json(csv_path: str) -> List[Dict[str, Any]]:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append({
                "pmid": (row.get("pmid") or "").strip() or None,
                "doi": (row.get("doi") or "").strip() or None,
                "title": (row.get("title") or "").strip(),
                "abstract": (row.get("abstract") or "").strip(),
                "journal": (row.get("journal") or "").strip() or None,
                "year": _parse_int(row.get("year")),
                "authors": _parse_list_field(row.get("authors")),
                "keywords": _parse_list_field(row.get("keywords")),
                "citation_count": _parse_int(row.get("citation_count")),
                "source": (row.get("source") or "").strip() or None,
                "url": (row.get("url") or "").strip() or None,
            })
    return rows

# ---------- node ----------
def extract(state: State) -> State:
    csv_path = state.get("csv_path") or "/Users/joan.estrada/Desktop/platzi-estudios/langraph_agentic_templates/notebooks/source_meridian/data/raw/pubmed_raw.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at {csv_path}")
    table_json = csv_to_table_json(csv_path)
    new_state: State = {**state, "table_json": table_json}
    return new_state