import requests

class KalshiClient:
    def __init__(self):
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"

    def get_markets(self):
        url = f"{self.base_url}/markets"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()

    def get_events(self):
        url = f"{self.base_url}/events"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()

    def get_series(self):
        url = f"{self.base_url}/series"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()

