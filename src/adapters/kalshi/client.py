# src/adapters/kalshi/client.py

import requests

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

def fetch_kalshi_markets() -> list[dict]:
    url = f"{BASE_URL}/markets"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json().get("markets", [])
