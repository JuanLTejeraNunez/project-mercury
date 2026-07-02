import requests
from .base_client import BaseDataClient

class PolymarketClient(BaseDataClient):
    """
    Cliente real para Polymarket usando la API pÃºblica CLOB.
    """

    MARKETS_URL = "https://clob.polymarket.com/markets"

    def get_markets(self):
        """
        Obtiene mercados reales desde Polymarket.
        La API devuelve un dict con clave 'data' que contiene la lista de mercados.
        """
        response = requests.get(self.MARKETS_URL)
        response.raise_for_status()
        raw = response.json()

        # La lista real de mercados estÃ¡ en raw["data"]
        return raw.get("data", [])

    def get_event(self, event_id):
        """
        Busca un mercado real por ID.
        """
        markets = self.get_markets()
        for m in markets:
            if str(m.get("id")) == str(event_id):
                return m
        return None

    def get_probability(self, event_id):
        """
        Probabilidad implÃ­cita real basada en precios.
        Polymarket usa precios de YES como probabilidad implÃ­cita.
        """
        market = self.get_event(event_id)
        if not market:
            return None

        yes_price = market.get("yes_price")
        if yes_price is None:
            return None

        return float(yes_price)

    def get_history(self, event_id):
        """
        Polymarket no expone historia en la API pÃºblica.
        """
        return {"history": []}
    def discover_markets(self):
        raw_markets = self.get_markets()
        markets = []
        for m in raw_markets:
            q = m.get("question", "").lower()
            if any(x in q for x in ["nfl","nba","mlb","nhl","ufc","mma"]):
                markets.append({
                    "source": "polymarket",
                    "market_id": m.get("condition_id") or m.get("id"),
                    "league": m.get("question"),
                    "season": 2026,
                    "home": "TBD",
                    "away": "TBD",
                    "notes": m.get("question", "").replace(",", " "),
                })
        return markets


