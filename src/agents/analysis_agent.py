# analysis_agent.py
"""
Agent de análisis: lee configs/sports_markets.csv, consulta probabilidades y calcula stake (Kelly).
Usa market_router.place_bet_for para ejecutar (respeta DRY_RUN).
"""
import os
import csv
from dotenv import load_dotenv
from src.integrations import market_router

load_dotenv()

DEFAULT_BANKROLL = float(os.getenv("DEFAULT_BANKROLL", "1000.0"))
DRY_RUN = os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes")

def kelly_fraction(p: float, b: float) -> float:
    q = 1.0 - p
    if b <= 0:
        return 0.0
    f = (b * p - q) / b
    return max(0.0, min(1.0, f))

def analyze_market_row(row):
    source = row.get("source")
    market_id = row.get("market_id")
    if not source or not market_id:
        print("Fila inválida en CSV:", row)
        return
    try:
        p = market_router.get_market_probability_for(source, market_id)
    except Exception as e:
        print(f"Error analyzing {source} {market_id}: {e}")
        return
    if p <= 0:
        print(f"[{source}] market {market_id}: no data (p={p})")
        return
    b = (1.0 / p) - 1.0
    f = kelly_fraction(p, b)
    stake = DEFAULT_BANKROLL * f
    print(f"[{source}] market={market_id} p={p:.4f} b={b:.4f} kelly={f:.4f} stake={stake:.2f}")
    # Example decision: if kelly fraction > 0.02, simulate placing an order
    if f > 0.02:
        client_order_id = f"auto-{source}-{market_id}"
        resp = market_router.place_bet_for(source, ticker=market_id, side="buy", count=1, price=p, client_order_id=client_order_id)
        if DRY_RUN:
            print(f"[DRY_RUN] simulated order: {resp}")
        else:
            print(f"[EXECUTED] order response: {resp}")

def run_once():
    cfg = os.path.join("configs", "sports_markets.csv")
    if not os.path.exists(cfg):
        print("No se encontró configs/sports_markets.csv. Crea el archivo con mercados.")
        return
    with open(cfg, newline="", encoding="utf-8") as f:
        reader = csv.DictReader([line for line in f if not line.strip().startswith("#")])
        for row in reader:
            analyze_market_row(row)

if __name__ == "__main__":
    run_once()


