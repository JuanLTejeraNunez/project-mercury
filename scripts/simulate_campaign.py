#!/usr/bin/env python3
"""
simulate_campaign.py
- Runs three paper-trading campaigns (A, B, C) using local episodes CSV/Parquet.
- Produces docs/decisions.jsonl and docs/campaign_report.md
"""
import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
from src.decision_engine import score_market, fractional_kelly, make_decision_card
from src.storage_adapters import write_jsonl_local

def load_market_list(path):
    return pd.read_csv(path)

def simple_selector(markets_df, capital, kelly_frac, max_stake_frac):
    # naive: compute model_p as price + 0.1 (mock model)
    markets = []
    for _, r in markets_df.iterrows():
        market_price = float(r["price"])
        model_p = min(0.99, market_price + 0.1)
        liquidity = float(r.get("liquidity") or 0)
        s = score_market(model_p, market_price, liquidity, volatility_factor=1.0)
        stake = fractional_kelly(model_p, market_price, frac=kelly_frac, cap_frac=max_stake_frac, capital=capital)
        markets.append((s, r["platform"], r["market_id"], r["market_url"], market_price, model_p, stake))
    markets = sorted([m for m in markets if m[0] > 0], key=lambda x: -x[0])
    return markets

def run_campaign(markets_df, campaign_name, capital, days, kelly_frac, max_stake_frac, reinvest_pct):
    decisions = []
    capital_t = capital
    for idx, m in enumerate(simple_selector(markets_df, capital_t, kelly_frac, max_stake_frac)[:10]):
        s, platform, market_id, market_url, price, model_p, stake = m
        stake = min(stake, capital_t * max_stake_frac)
        if stake < 0.01:
            continue
        side = "yes" if model_p > price else "no"
        expected_roi = (model_p - price) / max(1e-6, price)
        rationale = f"model_p={model_p:.3f} vs market={price:.3f}; score={s:.3f}"
        card = make_decision_card(platform, market_id, market_url, side, stake, stake*1.5, expected_roi, f"{days}d", rationale, {"model_p":model_p,"price":price,"liquidity":0}, reinvest_pct)
        decisions.append(card)
        # simulate immediate P&L: mock outcome by sampling with prob=model_p
        won = np.random.default_rng().random() < model_p
        payout = 1.0 if won else 0.0
        pnl = stake * (payout - 1.0)
        capital_t = capital_t + pnl + (pnl * reinvest_pct)  # simplistic reinvest
    return decisions, capital_t

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--market_csv", default="data/market_list_example.csv")
    parser.add_argument("--capital", type=float, default=100.0)
    parser.add_argument("--kelly_frac", type=float, default=0.1)
    parser.add_argument("--max_stake_frac", type=float, default=0.2)
    parser.add_argument("--days", type=int, default=4)
    args = parser.parse_args()

    markets_df = load_market_list(args.market_csv)
    campaigns = {
        "A_challenge": {"days":4, "target":"10x", "reinvest":0.95},
        "B_aggressive": {"days":4, "target":"3-5x", "reinvest":0.7},
        "C_daily_pct": {"days":7, "target":"+25%/day", "reinvest":0.85}
    }

    all_decisions = []
    report = {"campaigns": {}}
    for name, cfg in campaigns.items():
        decs, final_cap = run_campaign(markets_df, name, args.capital, cfg["days"], args.kelly_frac, args.max_stake_frac, cfg["reinvest"])
        all_decisions.extend(decs)
        report["campaigns"][name] = {"decisions": len(decs), "final_capital": final_cap}

    # write decisions to docs/decisions.jsonl
    write_jsonl_local("docs/decisions.jsonl", all_decisions)

    # write campaign report
    Path("docs").mkdir(parents=True, exist_ok=True)
    with open("docs/campaign_report.md", "w", encoding="utf-8") as f:
        f.write("# Campaign Report\\n\\n")
        f.write(json.dumps(report, indent=2))

    print("Simulation complete. Decisions and report written to docs/")
if __name__ == "__main__":
    main()
