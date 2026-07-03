#!/usr/bin/env python3
"""
Manual helper to mark resolutions for decisions in docs/decisions.jsonl.
Usage:
  python scripts/check_resolutions.py --decision_id <id> --result won|lost
"""
import argparse
import json
from pathlib import Path

DECISIONS = Path("docs/decisions.jsonl")
LOG = Path("docs/decisions_log.md")

def load_decisions():
    if not DECISIONS.exists():
        return []
    with open(DECISIONS, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f.read().splitlines() if l.strip()]

def save_decisions(decisions):
    with open(DECISIONS, "w", encoding="utf-8") as f:
        for d in decisions:
            f.write(json.dumps(d, ensure_ascii=False) + "\\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--decision_id", required=True)
    p.add_argument("--result", required=True, choices=["won","lost"])
    args = p.parse_args()
    decisions = load_decisions()
    found = False
    for d in decisions:
        if d.get("decision_id") == args.decision_id:
            d["result"] = args.result
            found = True
            LOG.write_text(LOG.read_text() + f"- {d.get('submitted_at')} | {args.decision_id} | result={args.result}\\n", encoding="utf-8")
            break
    if not found:
        print("Decision not found")
    else:
        save_decisions(decisions)
        print("Updated decision", args.decision_id)

if __name__ == "__main__":
    main()
