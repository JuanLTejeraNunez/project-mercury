#!/usr/bin/env python3
"""
prepare_data_local.py
- Minimal script to create a small episodes.parquet from data/market_list_example.csv
"""
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta

csv = Path("data/market_list_example.csv")
out = Path("data/processed/episodes.parquet")
if not csv.exists():
    print("Place data/market_list_example.csv first.")
    raise SystemExit(1)

df = pd.read_csv(csv)
rows = []
for _, r in df.iterrows():
    market_id = r["market_id"]
    price = float(r["price"])
    liquidity = float(r.get("liquidity") or 0)
    close_time = r["close_time"]
    # create a tiny timeline of 5 steps ending with resolution
    base = datetime.utcnow()
    for i in range(5):
        ts = (base + timedelta(minutes=i)).isoformat() + "Z"
        resolved = (i == 4)
        outcome = "yes" if np.random.rand() < price else "no"
        rows.append({"market_id": market_id, "ts": ts, "price": price, "liquidity": liquidity, "volume": 0, "resolved": resolved, "outcome": outcome})
df_out = pd.DataFrame(rows)
df_out.to_parquet(out, index=False)
print("Wrote", out)
