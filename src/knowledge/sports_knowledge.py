import re

# Diccionario de ligas por deporte
SPORT_LEAGUES = {
    'soccer': [
        'premier league', 'la liga', 'bundesliga', 'serie a', 'champions league',
        'ucl', 'mls', 'world cup', 'fifa', 'europa league'
    ],
    'basketball': [
        'nba', 'wnba', 'ncaa', 'euroleague', 'march madness'
    ],
    'baseball': [
        'mlb', 'world series'
    ],
    'football': [
        'nfl', 'super bowl'
    ],
    'hockey': [
        'nhl', 'stanley cup'
    ],
    'tennis': [
        'atp', 'wta', 'grand slam', 'wimbledon', 'roland garros',
        'us open', 'australian open'
    ],
    'mma': [
        'ufc', 'bellator'
    ],
    'boxing': [
        'wbc', 'wba', 'ibf'
    ]
}

# Diccionario de equipos por deporte
SPORT_TEAMS = {
    'soccer': [
        'barcelona', 'real madrid', 'manchester united', 'manchester city',
        'chelsea', 'liverpool', 'bayern', 'psg', 'juventus', 'inter'
    ],
    'basketball': [
        'lakers', 'warriors', 'celtics', 'bulls', 'heat', 'bucks'
    ],
    'baseball': [
        'yankees', 'dodgers', 'red sox', 'astros', 'cubs'
    ],
    'football': [
        'patriots', 'chiefs', 'cowboys', 'packers', 'eagles'
    ],
    'hockey': [
        'bruins', 'blackhawks', 'rangers', 'red wings'
    ]
}

def detect_league(text: str) -> str:
    text = text.lower()
    for sport, leagues in SPORT_LEAGUES.items():
        for league in leagues:
            if league in text:
                return league
    return 'unknown'

def detect_team(text: str) -> str:
    text = text.lower()
    for sport, teams in SPORT_TEAMS.items():
        for team in teams:
            if team in text:
                return team
    return 'unknown'

def enrich_market_info(title: str, ticker: str = "") -> dict:
    """
    Devuelve información enriquecida del mercado:
    - deporte detectado
    - liga detectada
    - equipo detectado
    """
    text = f"{title} {ticker}".lower()

    from src.knowledge.sports_classifier import classify_market

    sport = classify_market(title, ticker)
    league = detect_league(text)
    team = detect_team(text)

    return {
        'sport': sport,
        'league': league,
        'team': team
    }

