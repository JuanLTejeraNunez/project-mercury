# src/core/analysis_agent.py
"""
Mercury Analysis Agent: analiza mercados y genera señales básicas.
Funciones:
- analyze_market: analiza un mercado y devuelve una señal con métricas.
- analyze_markets: aplica analyze_market a una lista.
- filter_top_signals: filtra y ordena por signal_strength y priority_score.
"""

from __future__ import annotations

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

def analyze_market(market: Dict[str, Any]) -> Dict[str, Any]:
    """Analiza un mercado individual y genera una señal simple.

    Asegura tipos numéricos y devuelve un dict con campos esperados.
    """
    if not isinstance(market, dict):
        raise TypeError("market must be a dict")

    prob_yes = float(market.get("probability_yes", 0.0) or 0.0)
    prob_no = float(market.get("probability_no", 0.0) or 0.0)
    priority = float(market.get("priority_score", 0.0) or 0.0)
    expected_gain = float(market.get("expected_gain", 0.0) or 0.0)
    uncertainty = float(market.get("uncertainty_score", 0.0) or 0.0)

    # Señal compuesta: pesos explícitos y documentados
    signal_strength = (
        0.4 * priority +
        0.3 * expected_gain +
        0.3 * uncertainty
    )

    signal = {
        "market_id": market.get("market_id"),
        "source": market.get("source"),
        "category": market.get("category"),
        "probability_yes": prob_yes,
        "probability_no": prob_no,
        "priority_score": priority,
        "expected_gain": expected_gain,
        "uncertainty_score": uncertainty,
        "signal_strength": signal_strength,
    }

    logger.debug("analyze_market: %s -> strength=%.3f", signal.get("market_id"), signal_strength)
    return signal


def analyze_markets(markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analiza una lista de mercados y devuelve una lista de señales."""
    if not isinstance(markets, list):
        raise TypeError("markets must be a list")
    signals = []
    for m in markets:
        try:
            signals.append(analyze_market(m))
        except Exception:
            logger.exception("Failed to analyze market: %s", m)
    return signals


def filter_top_signals(signals: List[Dict[str, Any]], top_n: int = 50, min_priority: float = 0.0) -> List[Dict[str, Any]]:
    """Filtra las mejores señales según prioridad y fuerza.

    - Convierte priority a float para comparaciones seguras.
    - Ordena por signal_strength (desc) y priority_score (desc) como tie-breaker.
    """
    if not isinstance(signals, list):
        raise TypeError("signals must be a list")

    filtered = []
    for s in signals:
        try:
            priority = float(s.get("priority_score", 0.0) or 0.0)
            if priority >= float(min_priority):
                filtered.append(s)
        except Exception:
            logger.exception("Invalid signal format, skipping: %s", s)

    sorted_signals = sorted(
        filtered,
        key=lambda s: (float(s.get("signal_strength", 0.0) or 0.0), float(s.get("priority_score", 0.0) or 0.0)),
        reverse=True,
    )
    return sorted_signals[:int(top_n)]

