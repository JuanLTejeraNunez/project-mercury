from .kalshi_client import KalshiClient
from .kalshi_ws import KalshiWebSocket
from .models import KalshiMarket


class KalshiProvider:
    def __init__(self):
        self.client = KalshiClient()
        self.ws = KalshiWebSocket()

    def list_markets(self):
        raw = self.client.discover_markets()
        return [KalshiMarket(**m) for m in raw]

    def get_market(self, market_id: str):
        return self.client.get_market(market_id)

    def get_orderbook(self, market_id: str):
        return self.client.get_orderbook(market_id)

    async def stream_markets(self, tickers: list):
        async for update in self.ws.subscribe(tickers):
            yield update

