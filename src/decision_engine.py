"""
Decision engine baseline:
- score markets by (edge * log(1+liquidity) * volatility_factor)
- compute stake via fractional Kelly
"""
import math
import uuid
from datetime import datetime, timezone

def kelly_fraction(p: float, price: float):
    # price is market implied probability for "yes"
    # b = net odds = (1/price) - 1
    if price <= 0 or price >= 1:
        return 0.0
    b = (1.0 / price) - 1.0
    f_star = (b * p - (1 - p)) / b if b != 0 else 0.0
    return max(0.0, f_star)

def fractional_kelly(p: float, price: float, frac: float = 0.1, cap_frac: float = 0.2, capital: float = 100.0):
    f = kelly_fraction(p, price)
    f = f * frac
    stake = capital * f
    stake = min(stake, capital * cap_frac)
    return stake

def score_market(model_p: float, market_price: float, liquidity: float, volatility_factor: float = 1.0):
    edge = model_p - market_price
    if edge <= 0:
        return -9999.0
    return edge * math.log(1.0 + max(0.0, liquidity)) * volatility_factor

def make_decision_card(platform, market_id, market_url, side, stake_proposed, stake_max, expected_roi, time_horizon, rationale, key_signals, reinvest_if_win_pct, withdraw_if_cap_reaches=None):
    decision_id = str(uuid.uuid4())
    card = {
        "decision_id": decision_id,
        "platform": platform,
        "market_id": market_id,
        "market_url": market_url,
        "side": side,
        "stake_proposed": float(stake_proposed),
        "stake_max": float(stake_max),
        "expected_roi": float(expected_roi),
        "time_horizon": time_horizon,
        "rationale": rationale,
        "key_signals": key_signals,
        "reinvest_if_win_pct": float(reinvest_if_win_pct),
        "withdraw_if_cap_reaches": withdraw_if_cap_reaches,
        "submitted_at": datetime.now(timezone.utc).isoformat()
    }
    return card
