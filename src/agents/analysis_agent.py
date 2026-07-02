import logging
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from src.router.sports_market_router import SportsMarketRouter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class BetOpportunity:
    source: str
    market_id: str
    title: str
    recommended_side: str
    implied_prob: float
    model_prob: float
    edge: float
    max_stake: float


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _implied_prob_from_price(price_dollars: float) -> float:
    if price_dollars <= 0:
        return 0.0
    if price_dollars >= 1:
        return 1.0
    return price_dollars


def _model_probability_stub(market: Dict[str, Any]) -> float:
    liquidity = _safe_float(market.get("liquidity_dollars", 0.0))
    volume = _safe_float(market.get("volume_fp", market.get("volume_24h_fp", 0.0)))

    base = 0.5
    base += min(liquidity / 1000.0, 0.1)
    base += min(volume / 1000.0, 0.1)

    if base < 0.05:
        base = 0.05
    if base > 0.95:
        base = 0.95
    return base


def _build_kalshi_opportunities(markets, bankroll, min_edge, sport_filter=None):
    opportunities = []

    for m in markets:
        title = m.get("title", "")
        ticker = m.get("ticker", "")
        status = m.get("status", "")

        if status != "active":
            continue

        if sport_filter and sport_filter.lower() not in title.lower():
            continue

        yes_price = _safe_float(m.get("yes_ask_dollars", 0.0))
        no_price = _safe_float(m.get("no_ask_dollars", 0.0))

        implied_yes = _implied_prob_from_price(yes_price)
        implied_no = _implied_prob_from_price(no_price)

        model_prob = _model_probability_stub(m)

        edge_yes = model_prob - implied_yes
        edge_no = (1.0 - model_prob) - implied_no

        if edge_yes >= min_edge and edge_yes >= edge_no:
            recommended_side = "yes"
            edge = edge_yes
            implied = implied_yes
        elif edge_no >= min_edge:
            recommended_side = "no"
            edge = edge_no
            implied = implied_no
        else:
            continue

        max_stake = bankroll * min(edge * 2.0, 0.1)

        opportunities.append(
            BetOpportunity(
                source="kalshi",
                market_id=ticker,
                title=title,
                recommended_side=recommended_side,
                implied_prob=implied,
                model_prob=model_prob,
                edge=edge,
                max_stake=max_stake,
            )
        )

    return opportunities


def _build_polymarket_opportunities(markets, bankroll, min_edge, sport_filter=None):
    opportunities = []

    for m in markets:
        title = m.get("question", "")
        question_id = m.get("question_id", "")
        status = m.get("status", "open")

        if status != "open":
            continue

        if sport_filter and sport_filter.lower() not in title.lower():
            continue

        yes_price = _safe_float(m.get("yes_price", 0.0))
        implied_yes = _implied_prob_from_price(yes_price)
        model_prob = _model_probability_stub(m)

        edge_yes = model_prob - implied_yes

        if edge_yes < min_edge:
            continue

        max_stake = bankroll * min(edge_yes * 2.0, 0.1)

        opportunities.append(
            BetOpportunity(
                source="polymarket",
                market_id=question_id,
                title=title,
                recommended_side="yes",
                implied_prob=implied_yes,
                model_prob=model_prob,
                edge=edge_yes,
                max_stake=max_stake,
            )
        )

    return opportunities


def find_sports_opportunities(sport, bankroll, min_edge=0.02):
    router = SportsMarketRouter()
    all_markets = router.get_all_markets()

    kalshi_markets = all_markets.get("kalshi", []) or []
    poly_markets = all_markets.get("polymarket", []) or []

    kalshi_ops = _build_kalshi_opportunities(kalshi_markets, bankroll, min_edge, sport)
    poly_ops = _build_polymarket_opportunities(poly_markets, bankroll, min_edge, sport)

    opportunities = kalshi_ops + poly_ops
    opportunities.sort(key=lambda o: o.edge, reverse=True)

    return opportunities


def evaluate_and_place_bet(sport, event, entity_id, team_id, market_id, bankroll, min_edge=0.02):
    logger.info(
        "Evaluating opportunities: sport=%s event=%s entity_id=%s team_id=%s bankroll=%.2f",
        sport, event, entity_id, team_id, bankroll
    )

    opportunities = find_sports_opportunities(sport, bankroll, min_edge)

    if market_id:
        opportunities = [o for o in opportunities if o.market_id == market_id]

    result = {
        "sport": sport,
        "event": event,
        "entity_id": entity_id,
        "team_id": team_id,
        "bankroll": bankroll,
        "min_edge": min_edge,
        "opportunities": [asdict(o) for o in opportunities],
        "note": "Este agente identifica oportunidades cuantitativas, no ejecuta apuestas reales."
    }

    logger.info("Found %d opportunities", len(opportunities))
    return result


if __name__ == "__main__":
    demo = evaluate_and_place_bet(
        sport="soccer",
        event="demo",
        entity_id="demo_entity",
        team_id="demo_team",
        market_id=None,
        bankroll=1000.0,
        min_edge=0.02,
    )
    print(demo)
