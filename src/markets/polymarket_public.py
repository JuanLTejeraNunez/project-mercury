# src/markets/polymarket_public.py
"""
Polymarket public data helper (read-only).
Uses public endpoints to fetch market data without API key.
"""
import requests
from typing import Dict, Any

BASE_URL = "https://gateway.polymarket.com"

def get_market(market_id: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/markets/{market_id}"
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    return resp.json()

def get_market_probability(market_id: str) -> float:
    try:
        data = get_market(market_id)
        price = data.get("price") or data.get("probability") or 0.0
        return max(0.0, min(1.0, float(price)))
    except Exception:
        return 0.0


