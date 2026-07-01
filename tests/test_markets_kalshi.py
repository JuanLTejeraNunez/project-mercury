# tests/test_markets_kalshi.py
from src.markets import kalshi

def test_get_market_probability_handles_empty(monkeypatch):
    class FakeResp:
        def raise_for_status(self): pass
        def json(self): return {}
    def fake_req(method, url, headers=None, timeout=None, json=None, params=None):
        return FakeResp()
    monkeypatch.setattr("requests.request", fake_req)
    p = kalshi.get_market_probability("nonexistent")
    assert p == 0.0

