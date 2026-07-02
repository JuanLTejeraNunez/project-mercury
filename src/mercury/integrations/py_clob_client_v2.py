# src/mercury/integrations/py_clob_client_v2.py
# Stub mínimo para pruebas locales: py_clob_client_v2
# Provee ApiCreds y ClobClient con la interfaz básica usada por polymarket_client.

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ApiCreds:
    api_key: str
    api_secret: Optional[str] = None


class ClobClient:
    def __init__(self, creds: ApiCreds, base_url: str = "https://example.com"):
        self.creds = creds
        self.base_url = base_url

    def get_markets(self) -> Dict[str, Any]:
        """Devuelve una estructura mínima que imita la API real."""
        return {"markets": []}

    def get_orderbook(self, market_id: str) -> Dict[str, Any]:
        """Orderbook simulado."""
        return {"bids": [], "asks": [], "market_id": market_id}

    def place_order(self, market_id: str, side: str, size: float, price: float) -> Dict[str, Any]:
        """Simula colocar una orden y devuelve un resultado ficticio."""
        return {"status": "ok", "order_id": "stub-123", "market_id": market_id}

