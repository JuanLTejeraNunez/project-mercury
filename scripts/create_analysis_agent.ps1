# create_analysis_agent.ps1
# Crea carpetas necesarias y escribe el archivo analysis_agent.py usando here-string (método seguro)

# Crear carpeta src/knowledge si no existe (y __init__.py para que sea paquete)
New-Item -ItemType Directory -Path "src/knowledge" -Force | Out-Null

# Asegurar __init__.py para que Python trate src y src/knowledge como paquetes
New-Item -ItemType File -Path "src/__init__.py" -Force | Out-Null
New-Item -ItemType File -Path "src/knowledge/__init__.py" -Force | Out-Null

# Crear el archivo analysis_agent.py con contenido completo usando here-string
Set-Content -Path "analysis_agent.py" -Value @"
# analysis_agent.py
"""
Analysis Agent for Mercury
- Router de deportes
- Integracion de modulos de conocimiento por deporte
- Calculo de prob_internal, comparacion con mercado, edge, kelly, decision de apuesta
"""

import math
import importlib
import logging
from typing import Dict, Any, Callable

# Config logging simple
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("analysis_agent")

# -------------------------
# Router de deportes
# -------------------------
SPORT_MODULE_MAP = {
    "baseball": "src.knowledge.baseball.baseball_knowledge",
    "basketball": "src.knowledge.basketball.basketball_knowledge",
    "soccer": "src.knowledge.soccer.soccer_knowledge",
    "hockey": "src.knowledge.hockey.hockey_knowledge",
    "football": "src.knowledge.football.football_knowledge",
    "niche": "src.knowledge.niche.niche_knowledge",
}

# -------------------------
# Helpers: import dinamico
# -------------------------
def load_sport_module(sport: str):
    """
    Importa dinamicamente el modulo de conocimiento para el deporte.
    Devuelve el modulo o lanza ImportError si no existe.
    """
    module_path = SPORT_MODULE_MAP.get(sport)
    if not module_path:
        raise ValueError(f"Sport '{sport}' no soportado.")
    module = importlib.import_module(module_path)
    return module

# -------------------------
# Market data placeholder
# -------------------------
def get_market_probability(market_source: str, market_id: str) -> float:
    """
    Placeholder: obtiene la probabilidad del mercado para un evento.
    Reemplazar por integracion real (Polymarket, Kalshi, exchange API).
    Debe devolver un float entre 0 y 1.
    """
    if "low" in market_id:
        return 0.20
    if "mid" in market_id:
        return 0.50
    if "high" in market_id:
        return 0.80
    return 0.40

def market_odds_from_probability(p: float) -> float:
    """Convierte probabilidad p (0..1) a cuota decimal (odds). Evita division por cero."""
    if p <= 0:
        return float("inf")
    return 1.0 / p

# -------------------------
# Edge y Kelly
# -------------------------
def compute_edge(p_internal: float, p_market: float) -> float:
    """Edge simple: diferencia entre prob_internal y prob_market."""
    return p_internal - p_market

def kelly_fraction(p_internal: float, odds: float) -> float:
    """
    Kelly fraction (simplificado para apuestas a cuota decimal):
    f* = (bp - q) / b
    donde b = odds - 1, p = p_internal, q = 1 - p
    Si b <= 0 o resultado negativo -> 0
    """
    if odds <= 1:
        return 0.0
    b = odds - 1.0
    p = p_internal
    q = 1.0 - p
    numerator = b * p - q
    if numerator <= 0:
        return 0.0
    f = numerator / b
    return max(0.0, f)

# -------------------------
# Reglas de riesgo / filtros
# -------------------------
def apply_risk_limits(kelly_frac: float, edge: float, bankroll: float) -> float:
    """
    Aplica limites de riesgo:
    - cap maximo por apuesta (ej. 0.10 del bankroll)
    - cap conservador (ej. 0.05) si edge pequeño
    - escala por confianza (aqui simple: si edge < 0.05 -> reducir)
    """
    if kelly_frac <= 0:
        return 0.0

    # limites base
    max_cap = 0.10  # max 10% del bankroll
    conservative_cap = 0.05  # cap conservador

    # si edge pequeño, usar conservador
    if edge < 0.05:
        cap = conservative_cap
    else:
        cap = max_cap

    # aplicar cap al fraction (kelly_frac es fraccion del bankroll)
    final_frac = min(kelly_frac, cap)
    # adicional: no apostar mas del 50% del bankroll en ningun caso (seguridad)
    final_frac = min(final_frac, 0.5)
    return final_frac

# -------------------------
# Decision y ejecucion
# -------------------------
def evaluate_and_place_bet(
    sport: str,
    event: str,
    entity_id: str,
    team_id: str,
    market_source: str,
    market_id: str,
    bankroll: float,
    min_edge_threshold: float = 0.01
) -> Dict[str, Any]:
    """
    Flujo principal:
    - carga modulo del deporte
    - obtiene p_internal
    - obtiene p_market
    - calcula edge, odds, kelly
    - aplica limites de riesgo
    - decide apostar o no
    - devuelve dict con decision y detalles
    """
    # 1) cargar modulo
    module = load_sport_module(sport)

    # 2) obtener probabilidad interna
    compute_fn: Callable = getattr(module, "compute_internal_probability", None)
    if compute_fn is None:
        raise AttributeError(f"Modulo {sport} no expone compute_internal_probability")

    # Llamada al modulo (puede lanzar excepciones si la API falla; capturarlas arriba si se desea)
    p_internal = float(compute_fn(event, entity_id, team_id))
    logger.info(f"[{sport}] p_internal={p_internal:.4f}")

    # 3) obtener probabilidad del mercado
    p_market = float(get_market_probability(market_source, market_id))
    logger.info(f"[{sport}] p_market={p_market:.4f}")

    # 4) calcular edge y odds
    edge = compute_edge(p_internal, p_market)
    odds = market_odds_from_probability(p_market)
    logger.info(f"[{sport}] edge={edge:.4f}, odds={odds:.4f}")

    # 5) kelly
    kelly_frac = kelly_fraction(p_internal, odds)
    logger.info(f"[{sport}] raw_kelly_frac={kelly_frac:.4f}")

    # 6) aplicar limites de riesgo
    final_frac = apply_risk_limits(kelly_frac, edge, bankroll)
    stake = final_frac * bankroll
    logger.info(f"[{sport}] final_frac={final_frac:.4f}, stake={stake:.2f}")

    # 7) decision
    decision = "skip"
    if edge > min_edge_threshold and final_frac > 0:
        # Aqui se colocaria la orden real (place_bet) con integracion al exchange
        # Por ahora devolvemos la instruccion y simulamos la colocacion
        decision = "place_bet"
        logger.info(f"[{sport}] DECISION: PLACE BET stake={stake:.2f}")
    else:
        logger.info(f"[{sport}] DECISION: SKIP (edge={edge:.4f}, final_frac={final_frac:.4f})")

    return {
        "sport": sport,
        "event": event,
        "entity_id": entity_id,
        "team_id": team_id,
        "p_internal": p_internal,
        "p_market": p_market,
        "edge": edge,
        "odds": odds,
        "raw_kelly_frac": kelly_frac,
        "final_frac": final_frac,
        "stake": stake,
        "decision": decision,
    }

# -------------------------
# Ejemplo de uso (si se ejecuta como script)
# -------------------------
if __name__ == "__main__":
    # Ejemplo: simula una decision para baseball
    bankroll = 1000.0  # ejemplo
    result = evaluate_and_place_bet(
        sport="baseball",
        event="hit_today",
        entity_id="player_123",   # este id lo interpreta tu modulo
        team_id="team_abc",
        market_source="sim",
        market_id="low_example",  # usa "low","mid","high" para la simulacion
        bankroll=bankroll
    )
    print("RESULT:", result)
"@
