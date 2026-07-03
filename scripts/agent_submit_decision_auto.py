# scripts/agent_submit_decision_auto.py
import argparse, requests, json, uuid
parser = argparse.ArgumentParser()
parser.add_argument("--token", required=True)
args = parser.parse_args()
token = args.token
decision = {
    "market_id": "pm-automatic-test",
    "side": "yes",
    "stake_proposed": 5.0,
    "stake_max": 10.0,
    "expected_roi": 0.15,
    "time_horizon": "7 days",
    "rationale": "Automated test decision: example rationale.",
    "key_signals": {"model_score": 0.82, "price": 0.34, "volume": 1200},
    "decision_id": str(uuid.uuid4())
}
resp = requests.post("http://127.0.0.1:8000/submit_decision",
                     headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                     data=json.dumps(decision))
print("HTTP", resp.status_code)
print(resp.text)
