# src/core/engine.py
"""
Mercury Engine: carga datos desde adapters y produce un dataset unificado.
Responsabilidades:
- load_raw_data: invoca adapters y valida tipos.
- build_unified_dataset: normaliza y valida el dataset unificado.
- save_snapshot: guarda snapshot JSON serializable.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# Intentar importar adapters; si fallan, lanzar excepción clara.
try:
    from adapters.router import normalize_all_markets
    from adapters.polymarket.client import fetch_polymarket_markets
    from adapters.kalshi.client import fetch_kalshi_markets
except Exception as exc:  # pragma: no cover - environment dependent
    # No hacer import silencioso: dejar que el orquestador decida usar stubs.
    logger.debug("Adapters import failed in engine: %s", exc)
    # Re-raise to let caller handle fallback
    raise

def load_raw_data() -> Dict[str, List[Dict[str, Any]]]:
    """Carga datos crudos desde Polymarket y Kalshi. Devuelve dict de listas."""
    polymarket_markets = fetch_polymarket_markets()
    kalshi_markets = fetch_kalshi_markets()

    if not isinstance(polymarket_markets, list) or not isinstance(kalshi_markets, list):
        raise TypeError("Adapter fetch functions must return lists")

    return {
        "polymarket": polymarket_markets,
        "kalshi": kalshi_markets,
    }


def build_unified_dataset() -> List[Dict[str, Any]]:
    """Construye el dataset unificado normalizado.

    Lanza TypeError si normalize_all_markets no devuelve una lista.
    """
    raw = load_raw_data()
    normalized = normalize_all_markets(raw)

    if not isinstance(normalized, list):
        raise TypeError("normalize_all_markets must return a list")

    return normalized


def save_snapshot(markets: List[Dict[str, Any]], path: Optional[str] = "data_snapshot.json") -> None:
    """Guarda un snapshot JSON serializable en disco."""
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(markets),
        "markets": markets,
    }

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        logger.info("Snapshot saved to %s (markets=%d)", path, len(markets))
    except Exception as e:
        logger.exception("Failed to save snapshot to %s: %s", path, e)
        raise


def run_engine_once() -> List[Dict[str, Any]]:
    """Ejecuta el engine una vez: carga, normaliza y guarda snapshot."""
    markets = build_unified_dataset()
    logger.info("[ENGINE] Mercados normalizados: %d", len(markets))
    save_snapshot(markets)
    return markets


if __name__ == "__main__":  # pragma: no cover - script entry
    run_engine_once()
