import requests

def get_ncaa_football_stats(player_id, team_id):
    url = f"https://api.ncaa.com/football/player/{player_id}"
    r = requests.get(url).json()
    return {
        "event_rate": r.get("touchdowns_per_game", 0.5)
    }


