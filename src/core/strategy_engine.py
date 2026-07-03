# src/core/strategy_engine.py
"""
Mercury Strategy Engine: aplica reglas y genera decisiones simuladas.
Funciones:
- decide_action_for_signal: regla simple para decidir acción.
- generate_decisions: aplica la regla a una lista de señales.
- summarize_decisions: resumen agregando conteos por acción.
"""

from __future__ import annotations

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

def decide_action_for_signal(signal: Dict[str, Any]) -> Dict[str, Any]:
    """Decide una acción básica para una señal.

    Reglas:
    - strength < 0.1 -> ignore
    - prob_yes > 0.55 and priority > 5.0 -> consider_long_yes
    - prob_no > 0.55 and priority > 5.0 -> consider_long_no
    - else -> monitor
    """
    if not isinstance(signal, dict):
        raise TypeError("signal must be a dict")

    prob_yes = float(signal.get("probability_yes", 0.0) or 0.0)
    prob_no = float(signal.get("probability_no", 0.0) or 0.0)
    strength = float(signal.get("signal_strength", 0.0) or 0.0)
    priority = float(signal.get("priority_score", 0.0) or 0.0)

    if strength < 0.1:
        action = "ignore"
    elif prob_yes > 0.55 and priority > 5.0:
        action = "consider_long_yes"
    elif prob_no > 0.55 and priority > 5.0:
        action = "consider_long_no"
    else:
        action = "monitor"

    decision = {
        "market_id": signal.get("market_id"),
        "source": signal.get("source"),
        "category": signal.get("category"),
        "action": action,
        "signal_strength": strength,
        "priority_score": priority,
        "probability_yes": prob_yes,
        "probability_no": prob_no,
    }

    logger.debug("decide_action_for_signal: %s -> %s", decision.get("market_id"), action)
    return decision


def generate_decisions(signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Genera decisiones para una lista de señales."""
    if not isinstance(signals, list):
        raise TypeError("signals must be a list")
    decisions = []
    for s in signals:
        try:
            decisions.append(decide_action_for_signal(s))
        except Exception:
            logger.exception("Failed to generate decision for signal: %s", s)
    return decisions


def summarize_decisions(decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Genera un resumen simple de las decisiones."""
    if not isinstance(decisions, list):
        raise TypeError("decisions must be a list")
    summary = {
        "total": len(decisions),
        "actions_count": {},
    }

    for d in decisions:
        action = d.get("action", "unknown")
        summary["actions_count"][action] = summary["actions_count"].get(action, 0) + 1

    return summary
