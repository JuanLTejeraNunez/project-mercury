from pydantic import BaseModel
from typing import Optional


class KalshiMarket(BaseModel):
    source: str
    market_id: str
    ticker: str
    title: str
    category: Optional[str] = None
    season: Optional[int] = None
    league: Optional[str] = None
    home: Optional[str] = None
    away: Optional[str] = None
    notes: Optional[str] = None

