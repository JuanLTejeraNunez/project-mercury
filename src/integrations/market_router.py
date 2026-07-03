# src/integrations/market_router.py
import os
from typing import Any, Dict, Optional
from markets import kalshi, polymarket_public

DRY_RUN = os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes")

def get_market_probability_for(source: str, market_id: str, auth: Optional[Dict[str, str]] = None) -> float:
    if source == "kalshi":
        return kalshi.get_market_probability(market_id)
    if source == "polymarket":
        return polymarket_public.get_market_probability(market_id)
    raise ValueError(f"Unknown market source: {source}")

def place_bet_for(source: str, **kwargs) -> Dict[str, Any]:
    """
    Central guard for placing bets. Honors DRY_RUN env var.
    """
    if DRY_RUN:
        return {"status": "dry_run", "source": source, "request": kwargs}
    if source == "kalshi":
        return kalshi.place_order(kwargs["ticker"], kwargs["side"], kwargs["count"], kwargs["price"], kwargs["client_order_id"])
    raise ValueError(f"Place bet not implemented for source: {source}")



