# src/core/bet_manager.py
from __future__ import annotations
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
import threading
import logging
from typing import Optional, Dict, Any, List
import json
import os

logger = logging.getLogger(__name__)
DB_PATH = Path(os.getenv("MERCURY_DB_PATH", "data/mercury_bets.db"))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

CHECK_INTERVAL_SECONDS = int(os.getenv("MERCURY_BET_CHECK_INTERVAL", "60"))

class BetManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self._ensure_db()
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None

    def _conn(self):
        return sqlite3.connect(str(self.db_path), detect_types=sqlite3.PARSE_DECLTYPES)

    def _ensure_db(self):
        with self._conn() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS bets (
                bet_id TEXT PRIMARY KEY,
                market_id TEXT NOT NULL,
                side TEXT NOT NULL,
                stake REAL NOT NULL,
                placed_at TEXT NOT NULL,
                expected_close TEXT,
                status TEXT NOT NULL,
                result TEXT,
                result_snapshot TEXT,
                decision_reason TEXT,
                expected_roi REAL,
                time_horizon TEXT,
                stake_requested REAL,
                decision_metadata TEXT
            )
            """)
            conn.commit()

    def place_bet(self,
                  bet_id: str,
                  market_id: str,
                  side: str,
                  stake: float,
                  expected_close: Optional[str] = None,
                  decision_reason: Optional[str] = None,
                  expected_roi: Optional[float] = None,
                  time_horizon: Optional[str] = None,
                  stake_requested: Optional[float] = None,
                  decision_metadata: Optional[Dict[str, Any]] = None,
                  status: str = "open") -> None:
        """
        Place or update a bet. By default status='open' so agent-submitted decisions
        become active immediately. decision_metadata is stored as JSON.
        """
        placed_at = datetime.now(timezone.utc).isoformat()
        dm_json = json.dumps(decision_metadata, default=str, ensure_ascii=False) if decision_metadata is not None else None
        with self._conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO bets
                (bet_id, market_id, side, stake, placed_at, expected_close, status,
                 decision_reason, expected_roi, time_horizon, stake_requested, decision_metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (bet_id, market_id, side, float(stake), placed_at, expected_close, status,
                  decision_reason, expected_roi, time_horizon, stake_requested, dm_json))
            conn.commit()
        logger.info("Bet placed/updated: %s status=%s stake=%s reason=%s", bet_id, status, stake, decision_reason)

    def list_open_bets(self) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            cur = conn.execute("SELECT bet_id, market_id, side, stake, placed_at, expected_close, decision_reason, expected_roi, time_horizon, stake_requested FROM bets WHERE status = 'open'")
            rows = cur.fetchall()
        keys = ["bet_id","market_id","side","stake","placed_at","expected_close","decision_reason","expected_roi","time_horizon","stake_requested"]
        return [dict(zip(keys, r)) for r in rows]

    def list_decisions(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            cur = conn.execute("SELECT bet_id, market_id, side, stake, placed_at, decision_reason, expected_roi, time_horizon, stake_requested, decision_metadata, status, result FROM bets ORDER BY placed_at DESC LIMIT ?", (limit,))
            rows = cur.fetchall()
        keys = ["bet_id","market_id","side","stake","placed_at","decision_reason","expected_roi","time_horizon","stake_requested","decision_metadata","status","result"]
        out = []
        for r in rows:
            d = dict(zip(keys, r))
            if d.get("decision_metadata"):
                try:
                    d["decision_metadata"] = json.loads(d["decision_metadata"])
                except Exception:
                    d["decision_metadata"] = d["decision_metadata"]
            out.append(d)
        return out

    # The rest of the class (worker, checks) remains unchanged from previous version.
    def _fetch_market_snapshot(self, market_id: str) -> Dict[str, Any]:
        return {}

    def _determine_result(self, bet_row: Dict[str, Any], market_snapshot: Dict[str, Any]) -> Optional[str]:
        if not market_snapshot:
            return None
        if market_snapshot.get("resolved") is True:
            winner = market_snapshot.get("winner") or market_snapshot.get("outcome") or market_snapshot.get("result")
            if isinstance(winner, bool):
                winner = "yes" if winner else "no"
            if isinstance(winner, str):
                w = winner.lower()
                if w in ("yes","y","true","1"):
                    return "won" if bet_row["side"] == "yes" else "lost"
                if w in ("no","n","false","0"):
                    return "won" if bet_row["side"] == "no" else "lost"
        try:
            py = float(market_snapshot.get("probability_yes", market_snapshot.get("prob_yes", 0.0) or 0.0))
        except Exception:
            py = 0.0
        try:
            pn = float(market_snapshot.get("probability_no", market_snapshot.get("prob_no", 0.0) or 0.0))
        except Exception:
            pn = 0.0
        if py >= 0.999:
            return "won" if bet_row["side"] == "yes" else "lost"
        if pn >= 0.999:
            return "won" if bet_row["side"] == "no" else "lost"
        final = market_snapshot.get("final_result") or market_snapshot.get("resolution") or market_snapshot.get("final_outcome")
        if isinstance(final, str):
            f = final.lower()
            if f in ("yes","y","true","1"):
                return "won" if bet_row["side"] == "yes" else "lost"
            if f in ("no","n","false","0"):
                return "won" if bet_row["side"] == "no" else "lost"
        return None

    def _check_due_bets_once(self):
        now = datetime.now(timezone.utc)
        with self._conn() as conn:
            cur = conn.execute("SELECT bet_id, market_id, side, stake, expected_close FROM bets WHERE status = 'open'")
            rows = cur.fetchall()
        for r in rows:
            bet = dict(zip(["bet_id","market_id","side","stake","expected_close"], r))
            exp = bet.get("expected_close")
            if not exp:
                continue
            try:
                close_dt = datetime.fromisoformat(exp)
            except Exception:
                logger.warning("Invalid expected_close for bet %s: %s", bet["bet_id"], exp)
                continue
            if close_dt <= now:
                snapshot = self._fetch_market_snapshot(bet["market_id"])
                result = self._determine_result(bet, snapshot)
                if result in ("won","lost"):
                    with self._conn() as conn:
                        conn.execute("UPDATE bets SET status = ?, result = ?, result_snapshot = ? WHERE bet_id = ?",
                                     (result, result, json.dumps(snapshot, default=str, ensure_ascii=False), bet["bet_id"]))
                        conn.commit()
                    logger.info("Bet %s resolved -> %s", bet["bet_id"], result)
                else:
                    logger.info("Bet %s not yet resolvable; leaving open", bet["bet_id"])

    def start_worker(self, interval_seconds: int = CHECK_INTERVAL_SECONDS):
        if self._worker_thread and self._worker_thread.is_alive():
            logger.info("Worker already running")
            return
        self._stop_event.clear()
        def _run():
            logger.info("BetManager worker started (interval=%s)", interval_seconds)
            while not self._stop_event.is_set():
                try:
                    self._check_due_bets_once()
                except Exception:
                    logger.exception("Error checking bets")
                try:
                    stop_flag = Path("data") / "stop_worker"
                    if stop_flag.exists():
                        logger.info("Stop flag detected; exiting worker loop")
                        break
                except Exception:
                    logger.exception("Error checking stop flag")
                self._stop_event.wait(interval_seconds)
            logger.info("BetManager worker stopped")
        self._worker_thread = threading.Thread(target=_run, daemon=True, name="BetManagerWorker")
        self._worker_thread.start()

    def stop_worker(self):
        self._stop_event.set()
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
