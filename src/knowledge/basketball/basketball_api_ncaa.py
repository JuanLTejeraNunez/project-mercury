import requests

def get_ncaa_stats(player_id, team_id):
    url = f"https://api.collegebasketballreference.com/player/{player_id}"
    r = requests.get(url).json()
    return {
        "event_rate": r.get("points_per_game", 12.0)
    }

