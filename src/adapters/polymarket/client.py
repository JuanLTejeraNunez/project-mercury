# src/adapters/polymarket/client.py

import requests

BASE_URL = "https://gamma-api.polymarket.com"

def fetch_polymarket_markets(limit=1000) -> list[dict]:
    url = f"{BASE_URL}/markets?limit={limit}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()
