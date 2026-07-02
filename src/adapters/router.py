# src/adapters/router.py

from adapters.polymarket.normalizer import normalize_polymarket_market
from adapters.kalshi.normalizer import normalize_kalshi_market

def normalize_all_markets(raw_data: dict) -> list[dict]:
    """
    raw_data = {
        "polymarket": [...],
        "kalshi": [...],
        # En el futuro:
        # "robinhood": [...],
        # "nyse": [...],
        # "etoro": [...],
    }
    """

    normalized = []

    # Polymarket
    for m in raw_data.get("polymarket", []):
        normalized.append(normalize_polymarket_market(m))

    # Kalshi
    for m in raw_data.get("kalshi", []):
        normalized.extend(normalize_kalshi_market(m))

    return normalized
