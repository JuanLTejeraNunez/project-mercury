import logging

def evaluate_and_place_bet_from_market(market: dict, bankroll: float):
    # market viene de PolymarketClient/KalshiClient normalizado por Mercury
    p_market = market.get("p_market", 0.5)
    event = market.get("event", "unknown")
    source = market.get("source", "unknown")
    market_id = market.get("market_id", "unknown")

    # Ejemplo simple de probabilidad interna:
    p_internal = p_market  # aquí podrías aplicar tu modelo interno

    edge = p_internal - p_market
    stake = bankroll * 0.01 if edge > 0 else 0.0
    decision = "place_bet" if edge > 0 and stake > 0 else "skip"

    logging.info(
        f"[AnalysisAgent] source={source}, event={event}, market_id={market_id}, "
        f"p_market={p_market:.3f}, p_internal={p_internal:.3f}, edge={edge:.3f}, "
        f"decision={decision}, stake={stake:.2f}"
    )

    return {
        "sport": "unknown",
        "event": event,
        "entity_id": "unknown",
        "team_id": "unknown",
        "p_internal": p_internal,
        "p_market": p_market,
        "edge": edge,
        "stake": stake,
        "decision": decision,
        "market_id": market_id,
        "source": source
    }
