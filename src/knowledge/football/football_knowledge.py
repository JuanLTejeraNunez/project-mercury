from .football_api_nfl import get_nfl_stats
from .football_api_ncaa import get_ncaa_football_stats

def compute_internal_probability(event, player_id, team_id):
    nfl = get_nfl_stats(player_id, team_id)
    ncaa = get_ncaa_football_stats(player_id, team_id)
    avg_rate = (nfl["event_rate"] + ncaa["event_rate"]) / 2.0
    return avg_rate


