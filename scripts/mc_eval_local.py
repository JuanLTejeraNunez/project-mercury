#!/usr/bin/env python3
"""
mc_eval_local.py
- Simple Monte-Carlo evaluator that simulates final capital under iid daily returns with given r and sigma.
"""
import argparse
import numpy as np
import json
from pathlib import Path

def mc_sim(C0, r, sigma, days, iters):
    rng = np.random.default_rng(0)
    finals = []
    for _ in range(iters):
        c = C0
        for _ in range(days):
            daily = rng.normal(loc=r, scale=sigma)
            c = c * (1.0 + daily)
            if c <= 0:
                c = 0
                break
        finals.append(c)
    finals = np.array(finals)
    return {"mean_final": float(finals.mean()), "p_ge_target": float((finals >= 1300).mean()), "median": float(np.median(finals))}

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--C0", type=float, default=300.0)
    p.add_argument("--r", type=float, default=0.25)
    p.add_argument("--sigma", type=float, default=0.3)
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--iters", type=int, default=1000)
    args = p.parse_args()
    res = mc_sim(args.C0, args.r, args.sigma, args.days, args.iters)
    Path("docs").mkdir(parents=True, exist_ok=True)
    with open("docs/mc_result.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("Monte-Carlo result written to docs/mc_result.json")
