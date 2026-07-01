import requests

def get_rugby_stats(player_id, team_id):
    url = f"https://api.rugby.com/player/{player_id}"
    r = requests.get(url).json()
    return {
        "event_rate": r.get("tries_per_game", 0.5)
    }

