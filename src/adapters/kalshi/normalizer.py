# src/adapters/kalshi/normalizer.py

import math
import re
from datetime import datetime, timezone

# ==========================
# Helpers
# ==========================

def parse_iso(dt: str):
    if not dt:
        return None
    if dt.endswith("Z"):
        dt = dt[:-1]
    try:
        return datetime.fromisoformat(dt).replace(tzinfo=timezone.utc)
    except:
        return None


def compute_wait_time(end_time_iso: str):
    try:
        end = parse_iso(end_time_iso)
        if not end:
            return float("nan")
        now = datetime.now(timezone.utc)
        return (end - now).total_seconds() / 86400.0
    except:
        return float("nan")


# ==========================
# Inferencia de categoría
# ==========================

def infer_category_from_ticker(ticker: str) -> str:
    t = (ticker or "").upper()

    if re.search(r"KXMLB", t): return "baseball"
    if re.search(r"KXNBA", t): return "basketball"
    if re.search(r"KXNFL", t): return "football"
    if re.search(r"KXWC", t): return "soccer"
    if re.search(r"KXNHL", t): return "hockey"
    if re.search(r"KXTENNIS", t): return "tennis"
    if re.search(r"KXGOLF", t): return "golf"
    if re.search(r"KXMVESPORTSMULTIGAME", t): return "sports_multi"

    return "unknown"


# ==========================
# Incertidumbre
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
# Prioridad
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
# Expected Gain
# ==========================

def compute_expected_gain(market):
    py = float(market.get("probability_yes", 0.0))
    pn = float(market.get("probability_no", 0.0))
    return py * (1 - py) + pn * (1 - pn)


# ==========================
# Normalizador Kalshi
# ==========================

def normalize_kalshi_market(raw):
    """
    Si el mercado es multivariado (tiene legs), expandimos cada leg.
    Si no, normalizamos el mercado como binario simple.
    """
    legs = raw.get("mve_selected_legs", [])

    if not legs:
        return [_normalize_single(raw)]

    normalized = []
    for leg in legs:
        normalized.append(_normalize_single(raw, leg))
    return normalized


def _normalize_single(raw, leg=None):
    yes_bid = float(raw.get("yes_bid_dollars", 0.0))
    no_bid = float(raw.get("no_bid_dollars", 0.0))

    if leg:
        market_id = leg["market_ticker"]
        event_id = leg["event_ticker"]
        event_name = leg["market_ticker"]
        leg_side = leg["side"]
    else:
        market_id = raw["ticker"]
        event_id = raw["event_ticker"]
        event_name = raw["title"]
        leg_side = None

    market = {
        "source": "kalshi",
        "market_id": market_id,
        "event_id": event_id,
        "event_name": event_name,
        "category": infer_category_from_ticker(event_id),

        "description": raw.get("rules_primary", ""),

        "start_time": raw.get("open_time"),
        "end_time": raw.get("close_time"),
        "active": raw.get("status") == "active",
        "closed": raw.get("status") != "active",

        "outcomes": ["Yes", "No"],
        "prices": [yes_bid, no_bid],

        "probability_yes": yes_bid,
        "probability_no": no_bid,

        "liquidity": float(raw.get("liquidity_dollars", 0.0)),
        "volume": float(raw.get("volume_fp", 0.0)),

        "leg_side": leg_side,
    }

    market["wait_time_days"] = compute_wait_time(market["end_time"])
    market["uncertainty_score"] = compute_uncertainty(market)
    market["priority_score"] = compute_priority(market)
    market["expected_gain"] = compute_expected_gain(market)

    return market

