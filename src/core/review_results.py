import json
import os

OUTPUT_DIR = "outputs"
HISTORY_DIR = "history"

mercury_output_path = os.path.join(OUTPUT_DIR, "mercury_output.json")
resolved_markets_path = os.path.join(OUTPUT_DIR, "resolved_markets.json")
history_path = os.path.join(HISTORY_DIR, "mercury_results_history.json")

os.makedirs(HISTORY_DIR, exist_ok=True)

# Cargar oportunidades reales
with open(mercury_output_path, "r", encoding="utf-8-sig") as f:
    mercury_data = json.load(f)

# Cargar resultados simulados
with open(resolved_markets_path, "r", encoding="utf-8-sig") as f:
    resolved_data = json.load(f)

# Crear historial si no existe
if os.path.exists(history_path):
    with open(history_path, "r", encoding="utf-8-sig") as f:
        history = json.load(f)
else:
    history = []

# Procesar resultados
for result in resolved_data:
    market_id = result["market_id"]
    outcome = result["outcome"]

    for opp in mercury_data["opportunities"]:
        if opp["market_id"] == market_id:
            opp["result"] = outcome
            history.append(opp)

# Guardar historial actualizado
with open(history_path, "w", encoding="utf-8-sig") as f:
    json.dump(history, f, indent=4)

print("[OK] Resultados revisados y historial actualizado.")
