import logging
import requests
import json
from pathlib import Path

class PolymarketClient:
    def __init__(self, config_path: str = "config/mercury_config.json"):
        self.config = json.loads(Path(config_path).read_text())
        self.api_url = self.config.get("providers", {}).get("polymarket", {}).get("api_url", "")
        if not self.api_url:
            logging.warning("[PolymarketClient] api_url no definido en config.")

    def get_markets_raw(self):
        try:
            resp = requests.get(self.api_url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            logging.info(f"[PolymarketClient] Recibidos {len(data)} mercados crudos.")
            return data
        except Exception as e:
            logging.error(f"[PolymarketClient] Error al obtener mercados: {e}")
            return []

    def normalize_for_mercury(self, raw_markets):
        normalized = []
        for m in raw_markets:
            try:
                market_id = m.get("id") or m.get("market_id") or "unknown"
                question = m.get("question") or m.get("title") or "unknown"
                outcomes = m.get("outcomes") or []
                prices = m.get("prices") or []

                if not outcomes or not prices:
                    continue

                # Ejemplo simple: tomar primer outcome
                p_market = float(prices[0]) if prices else 0.5

                normalized.append({
                    "source": "polymarket",
                    "market_id": market_id,
                    "event": question,
                    "p_market": p_market,
                    "raw": m
                })
            except Exception as e:
                logging.warning(f"[PolymarketClient] Error normalizando mercado: {e}")
                continue

        logging.info(f"[PolymarketClient] Normalizados {len(normalized)} mercados para Mercury.")
        return normalized

    def get_markets_for_mercury(self):
        raw = self.get_markets_raw()
        return self.normalize_for_mercury(raw)
