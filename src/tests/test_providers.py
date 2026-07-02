import sys
import os
import logging

# AÑADIR src/ AL PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT)
sys.path.append(SRC)

logging.basicConfig(level=logging.INFO)

from providers.polymarket_client import PolymarketClient
from providers.kalshi_client import KalshiClient

print("\n==============================")
print("   TEST: POLYMARKET CLIENT")
print("==============================")

poly = PolymarketClient()

poly_raw = poly.get_markets_raw()
print(f"Polymarket RAW markets: {len(poly_raw)}")

poly_norm = poly.get_markets_for_mercury()
print(f"Polymarket normalized markets: {len(poly_norm)}")

if poly_raw:
    print("Polymarket está recibiendo datos ✔")
else:
    print("Polymarket NO está recibiendo datos ❌")


print("\n==============================")
print("   TEST: KALSHI CLIENT")
print("==============================")

kal = KalshiClient()

kal_raw = kal.get_markets_raw()
print(f"Kalshi RAW markets: {len(kal_raw)}")

kal_norm = kal.get_markets_for_mercury()
print(f"Kalshi normalized markets: {len(kal_norm)}")

if kal_raw:
    print("Kalshi está recibiendo datos ✔")
else:
    print("Kalshi NO está recibiendo datos ❌")

print("\n==============================")
print("   TEST COMPLETADO")
print("==============================\n")
