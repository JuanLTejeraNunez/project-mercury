import pytest
from mercury.data_providers.kalshi.kalshi_client import KalshiClient


def test_kalshi_client_init():
    client = KalshiClient()
    assert client.base_url.startswith("https://api.kalshi.com")


def test_discover_markets_structure(monkeypatch):
    class DummyResponse:
        def json(self):
            return {"events": [{
                "event_id": "SCIENCE.TEST",
                "event_ticker": "SCIENCE.TEST",
                "title": "Test Science Market",
                "category": "science"
            }]}
        @property
        def status_code(self):
            return 200

    def fake_request(method, url, headers=None, data=None):
        return DummyResponse()

    monkeypatch.setattr("requests.request", fake_request)

    client = KalshiClient()
    markets = client.discover_markets()
    assert len(markets) == 1
    assert markets[0]["category"] == "science"

