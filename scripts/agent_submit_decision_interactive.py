# scripts/agent_submit_decision_interactive.py
import argparse, requests, json, uuid
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument("--token", required=True)
args = parser.parse_args()
token = args.token

decision = {
    "market_id": "pm-12345",
    "side": "yes",
    "stake_proposed": None,
    "stake_max": 10.0,
    "expected_roi": None,
    "time_horizon": None,
    "rationale": "Momentum breakout after positive news; implied probability undervalued vs model.",
    "key_signals": {"model_score": 0.82, "price": 0.34, "volume": 1200},
    "decision_id": str(uuid.uuid4())
}

# Ask operator for missing fields
if decision["stake_proposed"] is None:
    decision["stake_proposed"] = float(input("Stake proposed (e.g., 5.0): ").strip())
if decision["expected_roi"] is None:
    decision["expected_roi"] = float(input("Expected ROI (decimal, e.g., 0.12): ").strip())
if decision["time_horizon"] is None:
    decision["time_horizon"] = input("Time horizon (e.g., '7 days' or ISO datetime): ").strip()

url = "http://127.0.0.1:8000/submit_decision"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
resp = requests.post(url, headers=headers, data=json.dumps(decision))
print("Status:", resp.status_code)
print(resp.text)
