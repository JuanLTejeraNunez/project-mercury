import os
import json
import time
import base64
import requests
from pathlib import Path
from typing import List

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

from dotenv import load_dotenv
load_dotenv()


class KalshiClient:
    def __init__(self):
        self.base_url = os.getenv("KALSHI_BASE_URL", "https://external-api.demo.kalshi.co")
        self.api_key_id = os.getenv("KALSHI_API_KEY_ID")
        self.private_key_path = os.getenv("KALSHI_PRIVATE_KEY_PATH")

        if not self.api_key_id:
            raise ValueError("KALSHI_API_KEY_ID no estÃ¡ definido en el entorno")

        if not self.private_key_path or not Path(self.private_key_path).exists():
            raise ValueError("KALSHI_PRIVATE_KEY_PATH no existe o no estÃ¡ definido")

        self.private_key = self._load_private_key()

    def _load_private_key(self):
        with open(self.private_key_path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def _sign(self, method: str, path: str, body: str = ""):
        timestamp = str(int(time.time()))
        message = f"{timestamp}.{method.upper()}.{path}.{body}"

        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

        return timestamp, base64.b64encode(signature).decode()

    def _request(self, method: str, endpoint: str, body=None):
        path = f"/v1/{endpoint}"
        body_json = json.dumps(body) if body else ""

        timestamp, signature = self._sign(method, path, body_json)

        headers = {
            "kalshi-api-key-id": self.api_key_id,
            "kalshi-signature": signature,
            "kalshi-timestamp": timestamp,
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}{path}"
        response = requests.request(method, url, headers=headers, data=body_json)

        if response.status_code >= 400:
            raise Exception(f"Kalshi API error {response.status_code}: {response.text}")

        return response.json()

    def discover_markets(self) -> List:
        data = self._request("GET", "events")
        markets = []

        for event in data.get("events", []):
            markets.append({
                "source": "kalshi",
                "market_id": event.get("event_id"),
                "ticker": event.get("event_ticker"),
                "title": event.get("title"),
            })

        return markets

    def get_market(self, market_id: str):
        return self._request("GET", f"markets/{market_id}")

    def get_orderbook(self, market_id: str):
        return self._request("GET", f"markets/{market_id}/orderbook")

    def get_trades(self, market_id: str):
        return self._request("GET", f"markets/{market_id}/trades")

    def get_positions(self):
        return self._request("GET", "positions")  # Solo en API real

    def get_balance(self):
        return self._request("GET", "balance")  # Solo en API real

    def create_order(self, market_id: str, side: str, price: float, size: int):
        body = {
            "market_id": market_id,
            "side": side,
            "price": price,
            "size": size
        }
        return self._request("POST", "orders", body)  # Solo en API real

    def cancel_order(self, order_id: str):
        return self._request("POST", "orders/cancel", {"order_id": order_id})  # Solo en API real

