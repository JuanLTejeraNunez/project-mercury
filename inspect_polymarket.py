import sys
import os
import json

# Añadir src/ al PYTHONPATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from providers.polymarket_client import PolymarketClient

pm = PolymarketClient()
markets = pm.get_markets_raw()

print("Total mercados:", len(markets))
print(json.dumps(markets[:3], indent=2))
