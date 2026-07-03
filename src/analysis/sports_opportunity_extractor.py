import math
from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime, timedelta

from knowledge.sports_classifier import is_sport_market
from knowledge.sports_knowledge import enrich_market_info
from analysis.probability_model import compute_probability


@dataclass
class Opportunity:
    source: str
    market_id: str
    title: str
    sport: str
    league: str
    team: str
    implied_prob: float
    model_prob: float
    edge: float
    recommended_side: str
    max_stake: float
    resolution_time: str
    expected_payout: float
    expected_return: float
    review_at: str
    result_status: str = "pending"
    bankroll_after_result: float = None


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except:
        return default


def _implied_prob(price: float) -> float:
    if price <= 0:
        return 0.0
    if price >= 1:
        return 1.0
    return price


def extract_opportunities(markets: List[Dict[str, Any]], bankroll: float, min_edge: float = 0.02) -> List[Opportunity]:
    opportunities = []

    for m in markets:
        title = m.get("title", m.get("question", ""))
        ticker = m.get("ticker", m.get("question_id", ""))

        if not is_sport_market(title, ticker):
            continue

        info = enrich_market_info(title, ticker)
        sport = info["sport"]
        league = info["league"]
        team = info["team"]

        yes_price = _safe_float(m.get("yes_ask_dollars", m.get("yes_price", 0)))
        no_price = _safe_float(m.get("no_ask_dollars", 0))

        implied_yes = _implied_prob(yes_price)
        implied_no = _implied_prob(no_price)

        model_prob = compute_probability(m)

        edge_yes = model_prob - implied_yes
        edge_no = (1.0 - model_prob) - implied_no

        if edge_yes >= min_edge and edge_yes >= edge_no:
            side = "yes"
            edge = edge_yes
            implied = implied_yes
        elif edge_no >= min_edge:
            side = "no"
            edge = edge_no
            implied = implied_no
        else:
            continue

        max_stake = bankroll * min(edge * 2.0, 0.1)

        resolution_time = m.get("resolution_time", "unknown")
        review_at = (datetime.utcnow() + timedelta(days=3)).isoformat()

        expected_payout = max_stake * edge
        expected_return = expected_payout / max_stake if max_stake > 0 else 0.0

        opportunities.append(
            Opportunity(
                source=m.get("source", "unknown"),
                market_id=ticker,
                title=title,
                sport=sport,
                league=league,
                team=team,
                implied_prob=implied,
                model_prob=model_prob,
                edge=edge,
                recommended_side=side,
                max_stake=max_stake,
                resolution_time=resolution_time,
                expected_payout=expected_payout,
                expected_return=expected_return,
                review_at=review_at,
            )
        )

    opportunities.sort(key=lambda o: o.edge, reverse=True)
    return opportunities


