from src.providers.kalshi_client import KalshiClient
from src.providers.polymarket_client import PolymarketClient

class SportsMarketRouter:
    def __init__(self):
        self.kalshi = KalshiClient()
        self.poly = PolymarketClient()

    def get_all_markets(self):
        kalshi = self.kalshi.get_markets()['markets']
        poly = self.poly.get_markets()
        return {
            'kalshi': kalshi,
            'polymarket': poly
        }


