from pathlib import Path
import json
import os

def read_parquet_local(path):
    import pandas as pd
    return pd.read_parquet(path)

def write_jsonl_local(path, records):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

# S3 stubs (implement when migrating)
def upload_to_s3_stub(local_path, s3_path):
    raise NotImplementedError("S3 adapter not implemented in local-first mode")
