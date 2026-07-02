# src/core/strategy_engine.py
# Mercury Strategy Engine: aplica reglas y genera decisiones simuladas.

def decide_action_for_signal(signal):
    """Decide una accion basica para una señal."""
    prob_yes = signal["probability_yes"]
    prob_no = signal["probability_no"]
    strength = signal["signal_strength"]
    priority = signal["priority_score"]

    if strength < 0.1:
        action = "ignore"
    elif prob_yes > 0.55 and priority > 5.0:
        action = "consider_long_yes"
    elif prob_no > 0.55 and priority > 5.0:
        action = "consider_long_no"
    else:
        action = "monitor"

    return {
        "market_id": signal["market_id"],
        "source": signal["source"],
        "category": signal["category"],
        "action": action,
        "signal_strength": strength,
        "priority_score": priority,
        "probability_yes": prob_yes,
        "probability_no": prob_no,
    }


def generate_decisions(signals):
    """Genera decisiones para una lista de señales."""
    decisions = []
    for s in signals:
        decisions.append(decide_action_for_signal(s))
    return decisions


def summarize_decisions(decisions):
    """Genera un resumen simple de las decisiones."""
    summary = {
        "total": len(decisions),
        "actions_count": {},
    }

    for d in decisions:
        action = d["action"]
        summary["actions_count"][action] = summary["actions_count"].get(action, 0) + 1

    return summary
