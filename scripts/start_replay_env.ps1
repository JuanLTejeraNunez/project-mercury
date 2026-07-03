python - <<'PY'
from pathlib import Path
import pandas as pd
from src.env.replay_env import ReplayEnv
p = Path("data/processed/episodes.parquet")
if not p.exists():
    print("Run scripts/prepare_data_local.py first.")
else:
    df = pd.read_parquet(p)
    env = ReplayEnv(df, seed=0)
    s = env.reset(0)
    print("Initial state:", s)
PY
