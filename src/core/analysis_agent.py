# src/core/analysis_agent.py
# Mercury Analysis Agent: analiza mercados y genera señales basicas.

def analyze_market(market):
    """Analiza un mercado individual y genera una señal simple."""
    prob_yes = float(market.get("probability_yes", 0.0))
    prob_no = float(market.get("probability_no", 0.0))
    priority = float(market.get("priority_score", 0.0))
    expected_gain = float(market.get("expected_gain", 0.0))
    uncertainty = float(market.get("uncertainty_score", 0.0))

    signal_strength = (
        0.4 * priority +
        0.3 * expected_gain +
        0.3 * uncertainty
    )

    return {
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


def analyze_markets(markets):
    """Analiza una lista de mercados y devuelve una lista de señales."""
    signals = []
    for m in markets:
        signals.append(analyze_market(m))
    return signals


def filter_top_signals(signals, top_n=50, min_priority=0.0):
    """Filtra las mejores señales segun prioridad y fuerza."""
    filtered = [
        s for s in signals
        if s["priority_score"] >= min_priority
    ]
    sorted_signals = sorted(
        filtered,
        key=lambda s: s["signal_strength"],
        reverse=True,
    )
    return sorted_signals[:top_n]
