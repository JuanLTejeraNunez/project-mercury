import json
import os
from agents.analysis_agent import evaluate_and_place_bet

# Ejecutar Mercury
result = evaluate_and_place_bet(
    sport='soccer',
    event='full_run',
    entity_id='auto',
    team_id='auto',
    market_id=None,
    bankroll=1000.0,
    min_edge=0.02,
)

# Crear carpeta outputs si no existe
os.makedirs('outputs', exist_ok=True)

# Exportar JSON
with open('outputs/mercury_output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4)

print("JSON exported to outputs/mercury_output.json")


