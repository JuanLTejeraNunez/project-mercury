# src/adapters/polymarket/normalizer.py

import json
import math
import re
from datetime import datetime, timezone

# ==========================
# Helpers de tiempo
# ==========================

def parse_iso(dt: str) -> datetime:
    if dt.endswith("Z"):
        dt = dt[:-1]
    return datetime.fromisoformat(dt).replace(tzinfo=timezone.utc)

def compute_wait_time(end_time_iso: str) -> float:
    try:
        end = parse_iso(end_time_iso)
        now = datetime.now(timezone.utc)
        return (end - now).total_seconds() / 86400.0
    except:
        return float("nan")

# ==========================
# Inferencia de categoría
# ==========================

def infer_category_from_question(question: str) -> str:
    q = question.lower()

    if re.search(r"nba|basketball", q): return "basketball"
    if re.search(r"mlb|baseball", q): return "baseball"
    if re.search(r"nfl|football", q): return "football"
    if re.search(r"world cup|euro|uefa|soccer", q): return "soccer"
    if re.search(r"bitcoin|btc|ethereum|eth|crypto", q): return "crypto"
    if re.search(r"election|president|senate|governor|primary", q): return "politics"
    if re.search(r"album|movie|release|celebrity|gta", q): return "entertainment"
    if re.search(r"inflation|cpi|jobs|unemployment|fed|interest rate", q): return "economy"

    return "unknown"

# ==========================
# Módulo de incertidumbre
# ==========================

def compute_uncertainty_from_prices(prices):
    if not prices:
        return 0.0

    s = sum(prices)
    if s <= 0:
        return 0.0

    probs = [p / s for p in prices]
    entropy = 0.0

    for p in probs:
        if p > 0:
            entropy -= p * math.log(p, 2)

    max_entropy = math.log(len(probs), 2) if len(probs) > 1 else 1.0
    return entropy / max_entropy

def compute_uncertainty(market):
    return compute_uncertainty_from_prices(market.get("prices", []))

# ==========================
# Módulo de prioridad
# ==========================

def compute_priority(market):
    liquidity = float(market.get("liquidity", 0.0))
    volume = float(market.get("volume", 0.0))
    wait_days = float(market.get("wait_time_days", 0.0))
    uncertainty = float(market.get("uncertainty_score", 0.0))

    liq_score = math.log(1 + liquidity)
    vol_score = math.log(1 + volume)
    wait_score = 1.0 / (1.0 + max(wait_days, 0))

    return (
        0.4 * liq_score +
        0.3 * vol_score +
        0.2 * wait_score +
        0.1 * uncertainty
    )

# ==========================
# Módulo de expected gain
# ==========================

def compute_expected_gain(market):
    py = float(market.get("probability_yes", 0.0))
    pn = float(market.get("probability_no", 0.0))

    return py * (1 - py) + pn * (1 - pn)

# ==========================
# Normalizador Polymarket
# ==========================

def normalize_polymarket_market(raw):
    try:
        outcomes = json.loads(raw.get("outcomes", "[]"))
    except:
        outcomes = []

    try:
        prices_raw = json.loads(raw.get("outcomePrices", "[]"))
        prices = [float(p) for p in prices_raw]
    except:
        prices_raw = []
        prices = []

    py = float(prices_raw[0]) if len(prices_raw) >= 1 else 0.0
    pn = float(prices_raw[1]) if len(prices_raw) >= 2 else 0.0

    market = {
        "source": "polymarket",
        "market_id": raw.get("id"),
        "event_id": raw.get("questionID"),
        "event_name": raw.get("question"),
        "category": infer_category_from_question(raw.get("question", "")),
        "description": raw.get("description", ""),

        "start_time": raw.get("startDate"),
        "end_time": raw.get("endDate"),
        "active": bool(raw.get("active", False)),
        "closed": bool(raw.get("closed", False)),

        "outcomes": outcomes,
        "prices": prices,

        "probability_yes": py,
        "probability_no": pn,

        "liquidity": float(raw.get("liquidityNum", 0.0)),
        "volume": float(raw.get("volumeNum", 0.0)),
    }

    market["wait_time_days"] = compute_wait_time(market["end_time"])
    market["uncertainty_score"] = compute_uncertainty(market)
    market["priority_score"] = compute_priority(market)
    market["expected_gain"] = compute_expected_gain(market)

    return market
