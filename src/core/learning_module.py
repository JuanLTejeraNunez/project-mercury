import json
import os
from learning_rules import should_learn, log_correction
from parameter_manager import load_parameters, save_parameters, update_parameter

history_path = "history/mercury_results_history.json"

def compute_brier(history):
    scores = []
    for h in history:
        p = h.get("predicted_prob")
        r = 1.0 if h.get("result") == "yes" else 0.0
        if p is not None:
            scores.append((p - r) ** 2)
    return sum(scores) / len(scores) if scores else None

def run_learning_cycle():
    if not os.path.exists(history_path):
        print("No history available")
        return

    with open(history_path, "r", encoding="utf-8-sig") as f:
        history = json.load(f)

    sample_size = len(history)
    params = load_parameters()

    # Compute old and new Brier
    brier_old = params.get("last_brier", 0.25)
    brier_new = compute_brier(history)

    allowed, reason = should_learn(sample_size, brier_old, brier_new)
    print("Learning decision:", reason)

    if not allowed:
        return

    # Example correction: reduce favorite bias
    old, new = update_parameter(params, "favorite_bias", params["favorite_bias"] * 0.95)
    save_parameters(params)

    log_correction("favorite_bias", old, new, reason, sample_size)

    params["last_brier"] = brier_new
    save_parameters(params)

    print("Learning applied")

if __name__ == "__main__":
    run_learning_cycle()
