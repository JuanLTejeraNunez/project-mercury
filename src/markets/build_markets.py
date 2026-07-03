import csv
from providers.polymarket_client import PolymarketClient
from providers.kalshi_client import KalshiClient

def build_markets_csv():
    markets = []

    try:
        poly = PolymarketClient()
        markets.extend(poly.discover_markets())
    except Exception as e:
        print("[WARN] Polymarket discovery failed:", e)

    try:
        kal = KalshiClient()
        markets.extend(kal.discover_markets())
    except Exception as e:
        print("[WARN] Kalshi discovery failed:", e)

    with open("configs/sports_markets.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source","market_id","league","season","home","away","notes"])
        writer.writeheader()
        writer.writerows(markets)

    print("CSV generado correctamente en configs/sports_markets.csv")

if __name__ == "__main__":
    build_markets_csv()



