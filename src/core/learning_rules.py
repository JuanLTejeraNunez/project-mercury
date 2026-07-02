import json
import os

# Learning rules module
# Ensures Mercury only learns when evidence is strong
# Prevents black-box behavior and uncontrolled corrections

def should_learn(sample_size, brier_old, brier_new):
    # Minimum sample size
    if sample_size < 50:
        return False, "Sample size too small"

    # Improvement threshold
    improvement = brier_old - brier_new
    if improvement < 0.05:
        return False, "Improvement too small"

    return True, "Learning allowed"

def log_correction(parameter, old, new, reason, sample_size):
    log_path = "history/learning_log.json"
    os.makedirs("history", exist_ok=True)

    entry = {
        "parameter": parameter,
        "old": old,
        "new": new,
        "reason": reason,
        "sample_size": sample_size
    }

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8-sig") as f:
            log = json.load(f)
    else:
        log = []

    log.append(entry)

    with open(log_path, "w", encoding="utf-8-sig") as f:
        json.dump(log, f, indent=4)

