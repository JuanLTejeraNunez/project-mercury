import sys
import os

# Agregar src/ al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


from adapters.router import normalize_all_markets
from adapters.polymarket.client import fetch_polymarket_markets
from adapters.kalshi.client import fetch_kalshi_markets

print("Descargando Polymarket...")
pm = fetch_polymarket_markets()

print("Descargando Kalshi...")
ks = fetch_kalshi_markets()

raw = {
    "polymarket": pm,
    "kalshi": ks
}

print("Normalizando...")
markets = normalize_all_markets(raw)

print(f"Mercados normalizados: {len(markets)}")

# Mostrar los primeros 3 para verificar
for m in markets[:3]:
    print("\n--- Mercado ---")
    for k, v in m.items():
        print(f"{k}: {v}")