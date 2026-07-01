import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()


class KalshiClient:
    def __init__(self):
        self.api_key = os.getenv("KALSHI_API_KEY_ID")
        self.base_url = "https://trading-api.kalshi.com"

        if not self.api_key:
            raise RuntimeError("KALSHI_API_KEY_ID no está definido en .env")

    def get_exchange_status(self):
        url = f"{self.base_url}/v1/exchange/status"

        headers = {
            "KALSHI-API-KEY-ID": self.api_key
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_markets(self):
        url = f"{self.base_url}/v1/markets"

        headers = {
            "KALSHI-API-KEY-ID": self.api_key
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()


def main():
    client = KalshiClient()

    print("=== Exchange Status ===")
    print(json.dumps(client.get_exchange_status(), indent=2))

    print("\n=== Markets ===")
    print(json.dumps(client.get_markets(), indent=2))


if __name__ == "__main__":
    main()
