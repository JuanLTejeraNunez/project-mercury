import logging
from providers.polymarket_client import PolymarketClient
from providers.kalshi_client import KalshiClient

class MarketRouter:
    def __init__(self, config_path: str = "config/mercury_config.json"):
        self.polymarket = PolymarketClient(config_path=config_path)
        self.kalshi = KalshiClient(config_path=config_path)

    def fetch_markets(self, sport: str):
        sport_lower = sport.lower()
        logging.info(f"[MarketRouter] fetch_markets llamado para sport={sport_lower}")

        # MLB / Baseball → Polymarket
        if sport_lower in ("mlb", "baseball"):
            markets = self.polymarket.get_markets_for_mercury()
            logging.info(f"[MarketRouter] Usando Polymarket para {sport_lower}, mercados={len(markets)}")
            return markets

        # NFL / Football → Kalshi
        if sport_lower in ("nfl", "football"):
            markets = self.kalshi.get_markets_for_mercury()
            logging.info(f"[MarketRouter] Usando Kalshi para {sport_lower}, mercados={len(markets)}")
            return markets

        # Default → Polymarket
        markets = self.polymarket.get_markets_for_mercury()
        logging.info(f"[MarketRouter] Sport desconocido, usando Polymarket por defecto, mercados={len(markets)}")
        return markets
