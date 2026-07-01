import csv
from src.markets.market import Market

def load_markets_from_csv(csv_path):
    markets = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            markets.append(
                Market(
                    source=row['source'],
                    market_id=row['market_id'],
                    league=row['league'],
                    season=int(row['season']),
                    home=row['home'],
                    away=row['away'],
                    notes=row['notes']
                )
            )
    return markets

