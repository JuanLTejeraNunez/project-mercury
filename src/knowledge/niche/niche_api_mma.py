import requests

def get_mma_stats(fighter_id):
    url = f"https://api.mma.com/fighter/{fighter_id}"
    r = requests.get(url).json()
    return {
        "event_rate": r.get("finish_rate", 0.5)
    }

