from .baseball_api_mlb import get_mlb_stats
from .baseball_api_espn import get_espn_stats
from .baseball_api_fangraphs import get_fangraphs_stats

def compute_internal_probability(event, player_id, team_id):
    mlb = get_mlb_stats(player_id, team_id)
    espn = get_espn_stats(player_id, team_id)
    fang = get_fangraphs_stats(player_id)
    avg_rate = (mlb["event_rate"] + espn["event_rate"] + fang["event_rate"]) / 3.0
    return avg_rate

