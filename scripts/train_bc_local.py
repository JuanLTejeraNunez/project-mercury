#!/usr/bin/env python3
"""
train_bc_local.py
- Behavior cloning skeleton: fits a tiny model to imitate baseline decisions.
This is a minimal placeholder that saves a checkpoint (JSON metadata).
"""
import json
from pathlib import Path
from datetime import datetime

out = Path("checkpoints")
out.mkdir(parents=True, exist_ok=True)
ckpt = {"policy_version": "bc_v1", "created_at": datetime.utcnow().isoformat(), "notes": "baseline BC checkpoint (placeholder)"}
with open(out / "policy_checkpoint.json", "w", encoding="utf-8") as f:
    json.dump(ckpt, f, indent=2)
print("Saved checkpoint", out / "policy_checkpoint.json")
