import logging
import json
from pathlib import Path

# Se asume que la clase original KalshiClient ya existe con su lógica interna:
# autenticación RSA-PSS, requests, endpoints, etc.
# Aquí solo se añade integración externa para Mercury.

class KalshiClient:
    def __init__(self, config_path: str = "config/mercury_config.json"):
        self.config = json.loads(Path(config_path).read_text())
        self.api_url = self.config.get("providers", {}).get("kalshi", {}).get("api_url", "")
        if not self.api_url:
            logging.warning("[KalshiClient] api_url no definido en config.")

        # Aquí se asume que ya tienes inicialización interna (keys, sesión, etc.)
        # No se toca esa lógica.

    def get_markets_raw(self):
        # IMPORTANTE:
        # Esta función debe llamar a tu lógica original interna que ya funciona.
        # Ejemplo:
        # return self._get_markets_from_kalshi()
        #
        # Como no modificamos tu lógica, aquí solo dejamos un placeholder.
        try:
            # TODO: conectar con tu implementación real existente.
            logging.info("[KalshiClient] get_markets_raw debe llamar a la implementación existente.")
            return []
        except Exception as e:
            logging.error(f"[KalshiClient] Error al obtener mercados: {e}")
            return []

    def normalize_for_mercury(self, raw_markets):
        normalized = []
        for m in raw_markets:
            try:
                market_id = m.get("id") or m.get("market") or "unknown"
                title = m.get("title") or m.get("question") or "unknown"

                # Ejemplo simple: usar yes_bid como probabilidad aproximada
                yes_bid = m.get("yes_bid")
                if yes_bid is None:
                    continue

                p_market = float(yes_bid)

                normalized.append({
                    "source": "kalshi",
                    "market_id": market_id,
                    "event": title,
                    "p_market": p_market,
                    "raw": m
                })
            except Exception as e:
                logging.warning(f"[KalshiClient] Error normalizando mercado Kalshi: {e}")
                continue

        logging.info(f"[KalshiClient] Normalizados {len(normalized)} mercados para Mercury.")
        return normalized

    def get_markets_for_mercury(self):
        raw = self.get_markets_raw()
        return self.normalize_for_mercury(raw)
# --- Añadido automáticamente por fix_providers.ps1 ---
from src.markets.kalshi import get_markets_public

def get_markets_raw(self):
    try:
        markets = get_markets_public()
        logging.info(f"[KalshiClient] Recibidos {len(markets)} mercados públicos desde Kalshi.")
        return markets
    except Exception as e:
        logging.error(f"[KalshiClient] Error al obtener mercados: {e}")
        return []
# --- Fin de bloque añadido ---
