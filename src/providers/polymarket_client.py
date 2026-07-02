import logging
import requests

class PolymarketClient:
    def __init__(self, api_url: str = "https://gamma-api.polymarket.com/markets"):
        self.api_url = api_url

    def get_markets_raw(self):
        """
        Descarga mercados públicos desde Polymarket (API Gamma).
        Devuelve JSON válido.
        """
        try:
            resp = requests.get(self.api_url, timeout=10)
            resp.raise_for_status()

            # La API Gamma devuelve una lista de mercados directamente
            markets = resp.json()

            logging.info(f"[PolymarketClient] Recibidos {len(markets)} mercados crudos.")
            return markets

        except Exception as e:
            logging.error(f"[PolymarketClient] Error al obtener mercados: {e}")
            return []

    def normalize_for_mercury(self, raw_markets):
        """
        Normaliza mercados para Mercury.
        """
        normalized = []
        for m in raw_markets:
            try:
                market_id = m.get("id") or "unknown"
                title = m.get("question") or m.get("title") or "unknown"

                yes_bid = (
                    m.get("yes_price")
                    or m.get("probability")
                    or m.get("midpoint")
                    or m.get("price")
                )

                if yes_bid is None:
                    continue

                normalized.append({
                    "source": "polymarket",
                    "market_id": market_id,
                    "event": title,
                    "p_market": float(yes_bid),
                    "raw": m
                })

            except Exception:
                continue

        logging.info(f"[PolymarketClient] Normalizados {len(normalized)} mercados para Mercury.")
        return normalized

    def get_markets_for_mercury(self):
        raw = self.get_markets_raw()
        return self.normalize_for_mercury(raw)


