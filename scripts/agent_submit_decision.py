# scripts/agent_submit_decision.py
"""
Ejemplo: el "agente" genera una Decision Card JSON y la envía al control API.
Uso:
  python scripts/agent_submit_decision.py --token <TOKEN>
"""
import argparse
import requests
import json
import uuid
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument("--token", required=True)
args = parser.parse_args()

token = args.token
url = "http://127.0.0.1:8000/submit_decision"
decision = {
    "market_id": "pm-12345",
    "side": "yes",
    "stake_proposed": 5.0,
    "stake_max": 10.0,
    "expected_roi": 0.15,
    "time_horizon": "7 days",
    "rationale": "Momentum breakout after positive news; implied probability undervalued vs model.",
    "key_signals": {"model_score": 0.82, "price": 0.34, "volume": 1200},
    "decision_id": str(uuid.uuid4())
}
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
resp = requests.post(url, headers=headers, data=json.dumps(decision))
print("Status:", resp.status_code)
print(resp.text)
