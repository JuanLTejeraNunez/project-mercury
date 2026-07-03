import math
from typing import Dict, Any

from knowledge.sports_classifier import classify_market
from knowledge.sports_knowledge import enrich_market_info


def _safe_float(v, default=0.0):
    try:
        return float(v)
    except:
        return default


def _normalize(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x


def compute_probability(market: Dict[str, Any]) -> float:
    """
    Modelo probabilístico avanzado de Mercury.
    Combina señales cuantitativas + deportivas + de mercado.
    Devuelve probabilidad en [0.05, 0.95].
    """

    # Señales cuantitativas
    liquidity = _safe_float(market.get('liquidity_dollars', 0))
    volume = _safe_float(market.get('volume_fp', market.get('volume_24h_fp', 0)))
    yes_price = _safe_float(market.get('yes_ask_dollars', market.get('yes_price', 0)))
    no_price = _safe_float(market.get('no_ask_dollars', 0))

    spread = abs(yes_price - (1 - no_price))
    spread_signal = max(0.0, 0.1 - spread)

    # Señales deportivas
    title = market.get('title', market.get('question', ''))
    ticker = market.get('ticker', market.get('question_id', ''))

    info = enrich_market_info(title, ticker)
    sport = info['sport']
    league = info['league']
    team = info['team']

    sport_signal = 0.05
    league_signal = 0.03
    team_signal = 0.03

    if sport != 'unknown':
        sport_signal += 0.05
    if league != 'unknown':
        league_signal += 0.05
    if team != 'unknown':
        team_signal += 0.05

    # Señales de mercado
    status = market.get('status', 'active')
    status_signal = 0.0 if status == 'active' else -0.05

    # Combinación de señales
    base = 0.5

    base += min(liquidity / 3000.0, 0.15)
    base += min(volume / 3000.0, 0.15)
    base += spread_signal

    base += sport_signal
    base += league_signal
    base += team_signal

    base += status_signal

    # Normalización final
    return _normalize(base, 0.05, 0.95)


