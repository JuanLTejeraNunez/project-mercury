"""
Minimal replay environment for paper-trading episodes.
Reads a precomputed episodes parquet with columns:
market_id, ts, price, liquidity, volume, resolved (bool), outcome (yes/no)
"""
from dataclasses import dataclass
import pandas as pd
import numpy as np
import json
from typing import Dict, Any, Optional

@dataclass
class StepResult:
    next_state: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]

class ReplayEnv:
    def __init__(self, episodes_df: pd.DataFrame, seed: int = 0, slippage_pct: float = 0.005, fee_pct: float = 0.0):
        self.episodes = episodes_df.sort_values("ts").reset_index(drop=True)
        self.slippage_pct = slippage_pct
        self.fee_pct = fee_pct
        self.rng = np.random.default_rng(seed)
        self.ptr = 0
        self.current_market = None
        self.done = False

    def reset(self, start_index: int = 0):
        self.ptr = start_index
        self.done = False
        row = self.episodes.iloc[self.ptr].to_dict()
        self.current_market = row["market_id"]
        state = {"ts": row["ts"], "price": row["price"], "liquidity": row.get("liquidity",0)}
        return state

    def step(self, action: Dict[str, Any]) -> StepResult:
        """
        action: {market_id, side, stake}
        Simulate immediate fill at current price with slippage and fees.
        """
        if self.done:
            return StepResult(None, 0.0, True, {})
        row = self.episodes.iloc[self.ptr].to_dict()
        price = float(row["price"])
        stake = float(action.get("stake", 0.0))
        # slippage model: proportional to 1/liquidity
        liquidity = float(row.get("liquidity") or 1.0)
        slippage = self.slippage_pct * (1.0 / max(1.0, liquidity/100.0))
        executed_price = price * (1 + slippage if action.get("side")=="yes" else 1 - slippage)
        # For binary markets, payout = 1 if outcome matches side, else 0
        reward = 0.0
        done = False
        info = {"executed_price": executed_price, "ts": row["ts"]}
        # advance pointer until resolution or end
        # if resolved at this row, compute reward
        if row.get("resolved") in (True, "true", 1):
            outcome = row.get("outcome")
            won = (outcome == action.get("side"))
            payout = 1.0 if won else 0.0
            gross = stake * payout
            fees = gross * self.fee_pct
            reward = gross - stake - fees
            done = True
        else:
            # not resolved yet: reward 0 and advance pointer
            reward = 0.0
            done = False
        # move pointer
        self.ptr += 1
        if self.ptr >= len(self.episodes):
            done = True
        next_state = None
        if not done:
            next_row = self.episodes.iloc[self.ptr].to_dict()
            next_state = {"ts": next_row["ts"], "price": next_row["price"], "liquidity": next_row.get("liquidity",0)}
        return StepResult(next_state, float(reward), bool(done), info)
