# --- Node: Classify medical specialty for each article ------------------------
from __future__ import annotations
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import json, math, random, re
import os
import pandas as pd

from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model

# Reuse your model config
llm = init_chat_model("openai:gpt-4o", temperature=0)

# --- State --------------------------------------------------------------------
class State(MessagesState):
    customer_name: str
    my_age: int
    table_json: List[Dict[str, Any]]
    labeled_table: List[Dict[str, Any]]

# --- Helpers ------------------------------------------------------------------
SPECIALTIES = [
    "Cardiology", "Oncology", "Neurology", "Pulmonology", "Endocrinology",
    "Rheumatology", "Orthopedics", "Gastroenterology", "Hematology",
    "Radiology", "Ophthalmology", "Nephrology", "Dermatology",
    "Infectious Disease", "Psychiatry", "Primary Care / General Medicine",
    "Pediatrics", "Obstetrics & Gynecology", "Emergency Medicine",
    "Pathology", "Surgery / General", "Urology", "Otolaryngology (ENT)"
]

KEYMAP = [
    (re.compile(r"\b(myocard|cardio|ECG|arrhythm|infarct|coronary)\b", re.I), "Cardiology"),
    (re.compile(r"\b(cancer|tumor|carcinoma|oncolog|neoplas|metastasis)\b", re.I), "Oncology"),
    (re.compile(r"\b(stroke|glioma|brain|neuro|parkinson|schizophren)\b", re.I), "Neurology"),
    (re.compile(r"\b(lung|pulmon|COPD|asthma|respirat|ventilator)\b", re.I), "Pulmonology"),
    (re.compile(r"\b(diabetes|endocrin|insulin|thyroid)\b", re.I), "Endocrinology"),
    (re.compile(r"\b(rheumat|arthritis|autoimmune|RA\b)\b", re.I), "Rheumatology"),
    (re.compile(r"\b(orthop|tibia|bone|fracture|spine|arthro)\b", re.I), "Orthopedics"),
    (re.compile(r"\b(colorectal|colitis|gastro|hepato|liver|GI\b)\b", re.I), "Gastroenterology"),
    (re.compile(r"\b(hemato|leukemia|lymphoma)\b", re.I), "Hematology"),
    (re.compile(r"\b(radiolog|CT|MRI|radiomic)\b", re.I), "Radiology"),
    (re.compile(r"\b(ophthal|retina|chorioretin|eye)\b", re.I), "Ophthalmology"),
    (re.compile(r"\b(nephro|kidney|renal)\b", re.I), "Nephrology"),
    (re.compile(r"\b(dermat|skin)\b", re.I), "Dermatology"),
    (re.compile(r"\b(infect|sepsis|antibiotic|viral|bacterial)\b", re.I), "Infectious Disease"),
    (re.compile(r"\b(psych|depress|bipolar|schizo|psychiatr)\b", re.I), "Psychiatry"),
    (re.compile(r"\b(pediatric|children|pediatric|childhood)\b", re.I), "Pediatrics"),
    (re.compile(r"\b(cervical|obstet|gyneco|pregnan)\b", re.I), "Obstetrics & Gynecology"),
    (re.compile(r"\b(urolog|prostate|renal cell)\b", re.I), "Urology"),
    (re.compile(r"\b(ent|otolaryng|head and neck)\b", re.I), "Otolaryngology (ENT)"),
    (re.compile(r"\b(surg(e?ry)?|operative|postoperative)\b", re.I), "Surgery / General"),
]

def heuristic_specialty(title: str, abstract: str) -> str:
    hay = f"{title or ''} {abstract or ''}"
    for rx, spec in KEYMAP:
        if rx.search(hay):
            return spec
    return "Primary Care / General Medicine"

def clamp_conf(p: Optional[float]) -> float:
    try:
        x = float(p)
    except:
        return 0.51
    return max(0.0, min(1.0, x))

def build_prompt(item: Dict[str, Any]) -> str:
    title = item.get("title", "") or ""
    abstract = item.get("abstract", "") or ""
    journal = item.get("journal", "") or ""
    doi = item.get("doi", "") or ""
    yr = item.get("year", "") or ""
    authors = ", ".join(item.get("authors", []) or [])
    return f"""
You are a medical literature triage assistant.

Task: Classify the specialty for the article and return strict JSON with keys:
- specialty: one of {SPECIALTIES}
- confidence: number between 0 and 1 (two decimals)
- reasoning: brief one-liner (<240 chars) citing cues (title/abstract)

Article:
Title: {title}
Abstract: {abstract}
Journal: {journal}
Year: {yr}
DOI: {doi}
Authors: {authors}

Output JSON only, no prose.
"""

def classify_one_with_llm(item: Dict[str, Any]) -> Tuple[str, float, str]:
    prompt = build_prompt(item)
    try:
        raw = llm.invoke(prompt)  # simple string prompt to avoid BaseMessage confusion
        txt = raw.content if hasattr(raw, "content") else str(raw)
        # Extract first {...} JSON block
        m = re.search(r"\{.*\}", txt, re.S)
        payload = json.loads(m.group(0)) if m else json.loads(txt)
        specialty = str(payload.get("specialty") or "").strip()
        confidence = clamp_conf(payload.get("confidence"))
        reasoning = str(payload.get("reasoning") or "").strip()

        if not specialty or specialty not in SPECIALTIES:
            raise ValueError("Invalid/unknown specialty from LLM")

        return specialty, confidence, reasoning

    except Exception:
        spec = heuristic_specialty(item.get("title"), item.get("abstract"))
        return spec, 0.62, "Heuristic keyword match from title/abstract."

# --- Node ---------------------------------------------------------------------
def classify_specialty_node(state: State) -> State:
    new_state: State = {}

    if state.get("customer_name") is None:
        new_state["customer_name"] = "Joan"
    else:
        new_state["my_age"] = random.randint(20, 50)

    table: List[Dict[str, Any]] = state.get("table_json") or []
    labeled: List[Dict[str, Any]] = []

    for item in table:
        specialty, confidence, reasoning = classify_one_with_llm(item)
        enriched = dict(item)
        enriched["specialty"]  = specialty
        enriched["confidence"] = round(confidence, 2)
        enriched["reasoning"]  = reasoning
        labeled.append(enriched)

    new_state["labeled_table"] = labeled


    # --- Persist CSV ----------------------------------------------------------
    output_path = "/Users/joan.estrada/Desktop/platzi-estudios/langraph_agentic_templates/src/agents/source_meridian/data/processed/pubmed_with_specialty.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.DataFrame(labeled)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"✅ Labeled CSV saved to: {output_path}")
    # --------------------------------------------------------------------------

    history = state.get("messages") or []
    ai_msg = f"Classified {len(labeled)} articles into specialties."
    print(ai_msg)
    new_state["messages"] = history + [ai_msg]
    return new_state