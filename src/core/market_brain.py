# src/core/market_brain.py
# Mercury Market Brain: orquesta engine, analisis y estrategia en un ciclo de sandbox.

import os
import sys
from datetime import datetime, timezone

# Asegurar que src este en el PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from core.engine import build_unified_dataset
from core.analysis_agent import analyze_markets, filter_top_signals
from core.strategy_engine import generate_decisions, summarize_decisions


def run_sandbox_cycle():
    """Ejecuta un ciclo completo de sandbox de Mercury."""
    print("[BRAIN] Iniciando ciclo de sandbox...")

    markets = build_unified_dataset()
    print(f"[BRAIN] Mercados cargados: {len(markets)}")

    signals = analyze_markets(markets)
    print(f"[BRAIN] Senales generadas: {len(signals)}")

    top_signals = filter_top_signals(signals, top_n=100, min_priority=5.0)
    print(f"[BRAIN] Top senales seleccionadas: {len(top_signals)}")

    decisions = generate_decisions(top_signals)
    summary = summarize_decisions(decisions)

    print("[BRAIN] Resumen de decisiones:")
    print(f"  Total decisiones: {summary['total']}")
    for action, count in summary["actions_count"].items():
        print(f"  {action}: {count}")

    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "markets_count": len(markets),
        "signals_count": len(signals),
        "top_signals_count": len(top_signals),
        "decisions": decisions,
        "summary": summary,
    }

    return snapshot


if __name__ == "__main__":
    run_sandbox_cycle()
