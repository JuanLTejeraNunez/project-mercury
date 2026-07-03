# src/control/api.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from pathlib import Path
import os
import threading
import uuid
import json
from datetime import datetime, timezone

from core.bet_manager import BetManager

app = FastAPI(title="Mercury BetManager Control API", version="0.4")

security = HTTPBearer(auto_error=False)

def require_token(creds: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    expected = os.getenv("CONTROL_API_TOKEN")
    if expected is None or creds is None or creds.scheme.lower() != "bearer" or creds.credentials != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

_bm_lock = threading.Lock()
_bm: Optional[BetManager] = None

def get_bm() -> BetManager:
    global _bm
    with _bm_lock:
        if _bm is None:
            _bm = BetManager()
        return _bm

class DecisionCard(BaseModel):
    market_id: str
    side: str
    stake_proposed: float
    stake_max: Optional[float] = None
    expected_roi: float
    time_horizon: str
    rationale: str
    key_signals: Optional[Dict[str, Any]] = None
    decision_id: Optional[str] = None

@app.post("/submit_decision", dependencies=[Depends(require_token)])
def submit_decision(card: DecisionCard):
    """
    Agent must submit a complete DecisionCard. The API will open the bet immediately
    (status=open) so the agent's behavior remains autonomous. We store decision metadata
    and append a human-readable log entry.
    """
    bm = get_bm()
    decision_id = card.decision_id or str(uuid.uuid4())
    bet_id = f"decision-{decision_id}"

    # Build metadata
    dm = {
        "key_signals": card.key_signals,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "stake_max": card.stake_max
    }

    # Place bet immediately using stake_proposed (agent autonomy preserved)
    bm.place_bet(bet_id=bet_id,
                 market_id=card.market_id,
                 side=card.side,
                 stake=card.stake_proposed,
                 expected_close=None,
                 decision_reason=card.rationale,
                 expected_roi=card.expected_roi,
                 time_horizon=card.time_horizon,
                 stake_requested=card.stake_proposed,
                 decision_metadata=dm,
                 status="open")

    # Append human-readable audit log
    try:
        Path("docs").mkdir(parents=True, exist_ok=True)
        log_line = f"- {datetime.now(timezone.utc).isoformat()} | decision_id={decision_id} | bet_id={bet_id} | market={card.market_id} | side={card.side} | stake={card.stake_proposed} | expected_roi={card.expected_roi} | horizon={card.time_horizon} | rationale={card.rationale}`n"
        with open("docs/decisions_log.md", "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass

    return {"message": "Decision submitted and bet opened", "decision_id": decision_id, "bet_id": bet_id}

@app.get("/decisions", dependencies=[Depends(require_token)])
def list_decisions(limit: int = 100):
    bm = get_bm()
    try:
        return bm.list_decisions(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ApproveRequest(BaseModel):
    decision_id: str
    stake: float
    expected_close: Optional[str] = None
    operator_note: Optional[str] = None

@app.post("/approve_decision", dependencies=[Depends(require_token)])
def approve_decision(req: ApproveRequest):
    """
    Approve endpoint kept for operator adjustments. If the bet already exists and is open,
    this endpoint can be used to update stake/expected_close and append operator notes.
    """
    bm = get_bm()
    bet_id = f"decision-{req.decision_id}"
    with bm._conn() as conn:
        cur = conn.execute("SELECT bet_id, market_id, side, stake_requested, decision_reason, expected_roi, time_horizon, decision_metadata FROM bets WHERE bet_id = ?", (bet_id,))
        rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Decision not found")
    row = rows[0]
    try:
        with bm._conn() as conn:
            # update stake and expected_close (if provided)
            conn.execute("UPDATE bets SET stake = ?, expected_close = ? WHERE bet_id = ?",
                         (float(req.stake), req.expected_close, bet_id))
            # append operator note to decision_metadata
            dm = row[7]
            try:
                dm_obj = json.loads(dm) if dm else {}
            except Exception:
                dm_obj = {"raw": dm}
            if req.operator_note:
                dm_obj.setdefault("operator_notes", []).append({"note": req.operator_note, "at": datetime.now(timezone.utc).isoformat()})
            dm_obj["approved_at"] = datetime.now(timezone.utc).isoformat()
            conn.execute("UPDATE bets SET decision_metadata = ? WHERE bet_id = ?", (json.dumps(dm_obj, default=str, ensure_ascii=False), bet_id))
            conn.commit()
        return {"message": "Decision approved and bet updated", "bet_id": bet_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bets", dependencies=[Depends(require_token)])
def list_bets():
    bm = get_bm()
    return bm.list_open_bets()

@app.get("/status", dependencies=[Depends(require_token)])
def status():
    bm = get_bm()
    wt = getattr(bm, "_worker_thread", None)
    running = bool(wt and wt.is_alive())
    return {"worker_running": running}

@app.post("/force_check", dependencies=[Depends(require_token)])
def force_check():
    bm = get_bm()
    bm._check_due_bets_once()
    return {"message": "Forced check executed"}

@app.post("/stop", dependencies=[Depends(require_token)])
def stop_worker():
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("data/stop_worker").write_text("stop")
    return {"message": "Stop flag created"}

@app.post("/start", dependencies=[Depends(require_token)])
def start_worker():
    bm = get_bm()
    wt = getattr(bm, "_worker_thread", None)
    if wt is not None and wt.is_alive():
        return {"message": "Worker already running"}
    bm.start_worker()
    return {"message": "Worker started"}
