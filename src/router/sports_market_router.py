import logging

from providers.polymarket_client import PolymarketClient
from providers.kalshi_client import KalshiClient

class SportsMarketRouter:
    """
    Router que decide qué proveedor usar según el deporte o categoría.
    """

    def __init__(self, config_path="config/mercury_config.json"):
        self.poly = PolymarketClient()
        self.kalshi = KalshiClient(config_path=config_path)

    def get_markets(self, sport: str):
        """
        Devuelve mercados normalizados para Mercury según el deporte.
        """

        sport_lower = sport.lower().strip()

        # Polymarket: deportes globales, política, cripto
        if sport_lower in ["soccer", "basketball", "mma", "boxing", "crypto", "politics", "global"]:
            logging.info(f"[MarketRouter] Usando Polymarket para {sport_lower}")
            return self.poly.get_markets_for_mercury()

        # Kalshi: deportes US, NFL, MLB, NBA, economía, elecciones US
        if sport_lower in ["nfl", "football", "mlb", "nba", "economy", "inflation", "elections"]:
            logging.info(f"[MarketRouter] Usando Kalshi para {sport_lower}")
            return self.kalshi.get_markets_for_mercury()

        # Default: Polymarket
        logging.info(f"[MarketRouter] Usando Polymarket (default) para {sport_lower}")
        return self.poly.get_markets_for_mercury()
