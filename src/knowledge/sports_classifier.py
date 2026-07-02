import re

SPORT_KEYWORDS = {
    'soccer': [
        'soccer', 'futbol', 'football', 'premier league', 'la liga', 'bundesliga',
        'serie a', 'champions league', 'ucl', 'mls', 'world cup', 'fifa'
    ],
    'basketball': [
        'basketball', 'nba', 'wnba', 'euroleague', 'ncaa', 'march madness'
    ],
    'baseball': [
        'baseball', 'mlb', 'world series', 'yankees', 'dodgers', 'red sox'
    ],
    'football': [
        'nfl', 'football', 'super bowl', 'patriots', 'chiefs', 'cowboys'
    ],
    'hockey': [
        'nhl', 'hockey', 'stanley cup', 'bruins', 'blackhawks'
    ],
    'tennis': [
        'tennis', 'atp', 'wta', 'grand slam', 'wimbledon', 'roland garros',
        'us open', 'australian open'
    ],
    'mma': [
        'ufc', 'mma', 'fight', 'bellator'
    ],
    'boxing': [
        'boxing', 'fight', 'wbc', 'wba', 'ibf'
    ]
}

def classify_market(title: str, ticker: str = "") -> str:
    """
    Clasifica un mercado deportivo basado en palabras clave.
    Devuelve el deporte detectado o 'unknown'.
    """
    text = f"{title} {ticker}".lower()

    for sport, keywords in SPORT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return sport

    return 'unknown'

def is_sport_market(title: str, ticker: str = "") -> bool:
    return classify_market(title, ticker) != 'unknown'

