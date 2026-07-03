from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import uuid

app = FastAPI(title="Mercury Local Control API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DECISIONS_JSONL = Path("docs/decisions.jsonl")

def append_decision(card: dict):
    DECISIONS_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(DECISIONS_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(card, ensure_ascii=False) + "\n")

@app.get("/decisions/latest")
def get_latest():
    if not DECISIONS_JSONL.exists():
        return {"decisions": []}
    with open(DECISIONS_JSONL, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    if not lines:
        return {"decisions": []}
    last = json.loads(lines[-1])
    return {"decision": last}

@app.get("/decisions/pending")
def list_pending():
    if not DECISIONS_JSONL.exists():
        return {"decisions": []}
    with open(DECISIONS_JSONL, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    cards = [json.loads(l) for l in lines]
    return {"decisions": cards}

@app.post("/decisions/approve")
def approve(payload: dict):
    # payload: {decision_id, operator_note}
    decision_id = payload.get("decision_id")
    operator_note = payload.get("operator_note")
    if not decision_id:
        raise HTTPException(status_code=400, detail="decision_id required")
    # append operator note to log file (human readable)
    log_line = f"- {decision_id} | approved | note={operator_note}\n"
    Path("docs/decisions_log.md").write_text(Path("docs/decisions_log.md").read_text() + log_line, encoding="utf-8")
    return {"message": "approved", "decision_id": decision_id}
