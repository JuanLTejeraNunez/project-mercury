# src/core/engine.py
# Mercury Engine: carga datos desde los adapters y produce un dataset unificado.

import os
import sys
from datetime import datetime, timezone

# Asegurar que src este en el PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from adapters.router import normalize_all_markets
from adapters.polymarket.client import fetch_polymarket_markets
from adapters.kalshi.client import fetch_kalshi_markets


def load_raw_data():
    """Carga datos crudos desde Polymarket y Kalshi."""
    polymarket_markets = fetch_polymarket_markets()
    kalshi_markets = fetch_kalshi_markets()

    return {
        "polymarket": polymarket_markets,
        "kalshi": kalshi_markets,
    }


def build_unified_dataset():
    """Construye el dataset unificado normalizado."""
    raw = load_raw_data()
    normalized = normalize_all_markets(raw)
    return normalized


def save_snapshot(markets, path="data_snapshot.json"):
    """Guarda un snapshot del dataset en disco."""
    import json

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(markets),
        "markets": markets,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def run_engine_once():
    """Ejecuta el engine una vez: carga, normaliza y guarda snapshot."""
    markets = build_unified_dataset()
    print(f"[ENGINE] Mercados normalizados: {len(markets)}")
    save_snapshot(markets)
    return markets


if __name__ == "__main__":
    run_engine_once()
