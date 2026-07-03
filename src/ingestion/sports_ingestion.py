import csv
from typing import List, Dict, Any

from knowledge.sports_classifier import classify_market, is_sport_market
from knowledge.sports_knowledge import enrich_market_info


def load_sports_csv(path: str) -> List[Dict[str, Any]]:
    """
    Carga sports_markets.csv y devuelve una lista de mercados normalizados.
    """
    markets = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            markets.append({
                'source': row.get('source', 'csv'),
                'market_id': row.get('market_id', ''),
                'title': row.get('title', ''),
                'yes_price': float(row.get('yes_price', 0)),
                'no_price': float(row.get('no_price', 0)),
                'liquidity_dollars': float(row.get('liquidity_dollars', 0)),
                'volume_fp': float(row.get('volume_fp', 0)),
                'status': row.get('status', 'active')
            })
    return markets


def enrich_csv_markets(markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enriquecer mercados del CSV con conocimiento deportivo.
    """
    enriched = []
    for m in markets:
        title = m.get('title', '')
        ticker = m.get('market_id', '')

        if not is_sport_market(title, ticker):
            continue

        info = enrich_market_info(title, ticker)

        m['sport'] = info['sport']
        m['league'] = info['league']
        m['team'] = info['team']

        enriched.append(m)

    return enriched


def load_and_enrich_csv(path: str) -> List[Dict[str, Any]]:
    """
    Pipeline completo:
    - carga CSV
    - filtra mercados deportivos
    - enriquece con conocimiento deportivo
    """
    raw = load_sports_csv(path)
    enriched = enrich_csv_markets(raw)
    return enriched


