<#
    fix_kalshi_client.ps1
    Reemplaza completamente src/providers/kalshi_client.py
    para usar get_markets_public() correctamente.
#>

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$kalshiClientPath = "src/providers/kalshi_client.py"

Write-Host "Reemplazando archivo completo: $kalshiClientPath ..."

@"
import logging
import json
from pathlib import Path

# Import correcto del módulo limpio
from markets.kalshi import get_markets_public

class KalshiClient:
    def __init__(self, config_path: str = "config/mercury_config.json"):
        self.config = json.loads(Path(config_path).read_text())
        self.api_url = self.config.get("providers", {}).get("kalshi", {}).get("api_url", "")
        if not self.api_url:
            logging.warning("[KalshiClient] api_url no definido en config.")

    def get_markets_raw(self):
        \"\"\"
        Obtiene mercados públicos desde Kalshi.
        No usa autenticación.
        \"\"\"
        try:
            markets = get_markets_public()
            logging.info(f"[KalshiClient] Recibidos {len(markets)} mercados públicos desde Kalshi.")
            return markets
        except Exception as e:
            logging.error(f"[KalshiClient] Error al obtener mercados: {e}")
            return []

    def normalize_for_mercury(self, raw_markets):
        normalized = []
        for m in raw_markets:
            try:
                market_id = m.get("id") or m.get("market") or "unknown"
                title = m.get("title") or m.get("question") or "unknown"

                yes_bid = (
                    m.get("midpoint")
                    or m.get("price")
                    or m.get("last_price")
                    or m.get("probability")
                )

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
"@ | Set-Content $kalshiClientPath

Write-Host "Archivo reemplazado correctamente."
