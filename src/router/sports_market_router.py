from src.providers.polymarket_client import PolymarketClient
from src.providers.kalshi_client import KalshiClient

ROUTER = {
    "polymarket": PolymarketClient(),
    "kalshi": KalshiClient(),
}

def get_client(source: str):
    return ROUTER[source]

