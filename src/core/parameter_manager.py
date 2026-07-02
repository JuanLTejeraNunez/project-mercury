import json
import os

# Parameter manager
# Stores Mercury parameters and applies safe updates

config_path = "config/mercury_config.json"

def load_parameters():
    if not os.path.exists(config_path):
        return {
            "favorite_bias": 0.15,
            "underdog_bias": 0.10,
            "kelly_fraction": 0.50
        }
    with open(config_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save_parameters(params):
    os.makedirs("config", exist_ok=True)
    with open(config_path, "w", encoding="utf-8-sig") as f:
        json.dump(params, f, indent=4)

def update_parameter(params, key, new_value):
    old_value = params[key]
    params[key] = new_value
    return old_value, new_value

