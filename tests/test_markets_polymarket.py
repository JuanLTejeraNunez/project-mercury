# tests/test_markets_polymarket.py
from markets import polymarket_public

def test_get_market_probability_parses_price(monkeypatch):
    class FakeResp:
        def raise_for_status(self): pass
        def json(self): return {"price": 0.42}
    def fake_get(url, timeout=None):
        return FakeResp()
    monkeypatch.setattr("requests.get", fake_get)
    p = polymarket_public.get_market_probability("m1")
    assert abs(p - 0.42) < 1e-6



