import requests

def get_mlb_stats(player_id, team_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
    r = requests.get(url).json()
    return {
        "event_rate": r.get("stats", [{}])[0].get("splits", [{}])[0].get("stat", {}).get("avg", 0.1)
    }

