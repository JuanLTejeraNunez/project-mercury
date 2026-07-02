from .soccer_api_fifa import get_fifa_stats
from .soccer_api_openfooty import get_openfooty_stats

def compute_internal_probability(event, player_id, team_id):
    fifa = get_fifa_stats(player_id, team_id)
    openfooty = get_openfooty_stats(player_id, team_id)
    avg_rate = (fifa["event_rate"] + openfooty["event_rate"]) / 2.0
    return avg_rate


