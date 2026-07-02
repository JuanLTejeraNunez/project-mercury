import os
import json
import time
import base64
import asyncio
import websockets
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from dotenv import load_dotenv
load_dotenv()


class KalshiWebSocket:
    WS_URL = "wss://api.kalshi.com/ws/v1"

    def __init__(self):
        self.api_key_id = os.getenv("KALSHI_API_KEY_ID")
        private_key_path = os.getenv("KALSHI_PRIVATE_KEY_PATH")

        if not self.api_key_id:
            raise ValueError("KALSHI_API_KEY_ID no está definido en el entorno")

        if not private_key_path or not Path(private_key_path).exists():
            raise ValueError("KALSHI_PRIVATE_KEY_PATH no existe o no está definido")

        with open(private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(f.read(), password=None)

    def _sign(self, message: str):
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return base64.b64encode(signature).decode()

    async def subscribe(self, markets: list):
        timestamp = str(int(time.time()))
        market_list = ",".join(markets)

        message = f"{timestamp}.WS.SUBSCRIBE.{market_list}"
        signature = self._sign(message)

        headers = {
            "kalshi-api-key-id": self.api_key_id,
            "kalshi-signature": signature,
            "kalshi-timestamp": timestamp,
        }

        async with websockets.connect(self.WS_URL, extra_headers=headers) as ws:
            await ws.send(json.dumps({
                "type": "subscribe",
                "markets": markets
            }))

            while True:
                msg = await ws.recv()
                yield json.loads(msg)


