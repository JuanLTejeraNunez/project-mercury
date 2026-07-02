# Stats fetcher
# Placeholder module for fetching external stats and context
# Later can be extended to call real APIs (Elo ratings, xG, injuries, etc.)

def get_team_context(team_name):
    # Returns a simple context dict for now
    # In future: integrate real data sources
    return {
        "team": team_name,
        "elo_rating": None,
        "recent_form": None,
        "injuries": [],
        "notes": "Context placeholder. Replace with real data sources."
    }
