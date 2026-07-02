import requests

def get_nba_stats(player_id, team_id):
    url = f"https://api-nba-v1.p.rapidapi.com/players/statistics?player={player_id}"
    headers = {"X-RapidAPI-Key": "YOUR_KEY_HERE"}
    r = requests.get(url, headers=headers).json()
    return {
        "event_rate": r.get("response", [{}])[0].get("points", 10.0)
    }


