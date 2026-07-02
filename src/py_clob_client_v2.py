from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class ApiCreds:
    api_key: str
    api_secret: Optional[str] = None
    api_passphrase: Optional[str] = None
    deposit_wallet: Optional[str] = None

class ClobClient:
    def __init__(self, creds: ApiCreds, base_url: str = "https://example.com"):
        self.creds = creds
        self.base_url = base_url

    def get_markets(self) -> Dict[str, Any]:
        return {"markets": []}

    def get_orderbook(self, market_id: str) -> Dict[str, Any]:
        return {"bids": [], "asks": [], "market_id": market_id}

    def place_order(self, market_id: str, side: str, size: float, price: float) -> Dict[str, Any]:
        return {"status": "ok", "order_id": "stub-123", "market_id": market_id}

