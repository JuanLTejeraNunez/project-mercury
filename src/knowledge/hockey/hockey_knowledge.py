from .hockey_api_nhl import get_nhl_stats

def compute_internal_probability(event, player_id, team_id):
    nhl = get_nhl_stats(player_id, team_id)
    return nhl["event_rate"]


