from .basketball_api_nba import get_nba_stats
from .basketball_api_ncaa import get_ncaa_stats

def compute_internal_probability(event, player_id, team_id):
    nba = get_nba_stats(player_id, team_id)
    ncaa = get_ncaa_stats(player_id, team_id)
    avg_rate = (nba["event_rate"] + ncaa["event_rate"]) / 2.0
    return avg_rate


