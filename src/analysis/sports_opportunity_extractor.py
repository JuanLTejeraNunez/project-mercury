import math
from dataclasses import dataclass
from typing import Dict, Any, List

from src.knowledge.sports_classifier import classify_market, is_sport_market
from src.knowledge.sports_knowledge import enrich_market_info


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


def _model_probability(market: Dict[str, Any]) -> float:
    """
    Modelo avanzado:
    - liquidez
    - volumen
    - status
    - sport knowledge
    """
    liquidity = _safe_float(market.get("liquidity_dollars", 0))
    volume = _safe_float(market.get("volume_fp", market.get("volume_24h_fp", 0)))
    status = market.get("status", "active")

    base = 0.5

    # Liquidez → más información
    base += min(liquidity / 2000.0, 0.15)

    # Volumen → más participantes
    base += min(volume / 2000.0, 0.15)

    # Mercados cerrados → menos confiables
    if status != "active":
        base -= 0.1

    # Clamp
    return max(0.05, min(base, 0.95))


def extract_opportunities(markets: List[Dict[str, Any]], bankroll: float, min_edge: float = 0.02) -> List[Opportunity]:
    """
    Extrae oportunidades deportivas avanzadas:
    - Clasificación deportiva
    - Enriquecimiento de mercado
    - Edge avanzado
    - Recomendación de lado
    - Cálculo de stake
    """
    opportunities = []

    for m in markets:
        title = m.get("title", m.get("question", ""))
        ticker = m.get("ticker", m.get("question_id", ""))

        # Clasificación deportiva
        if not is_sport_market(title, ticker):
            continue

        info = enrich_market_info(title, ticker)
        sport = info["sport"]
        league = info["league"]
        team = info["team"]

        # Precios
        yes_price = _safe_float(m.get("yes_ask_dollars", m.get("yes_price", 0)))
        no_price = _safe_float(m.get("no_ask_dollars", 0))

        implied_yes = _implied_prob(yes_price)
        implied_no = _implied_prob(no_price)

        model_prob = _model_probability(m)

        edge_yes = model_prob - implied_yes
        edge_no = (1.0 - model_prob) - implied_no

        # Selección del lado
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

        # Stake basado en Kelly-like
        max_stake = bankroll * min(edge * 2.0, 0.1)

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
            )
        )

    # Ordenar por edge descendente
    opportunities.sort(key=lambda o: o.edge, reverse=True)
    return opportunities
