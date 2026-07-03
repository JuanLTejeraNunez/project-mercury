import json
from src.agents.analysis_agent import evaluate_and_place_bet

if __name__ == '__main__':
    result = evaluate_and_place_bet(
        sport='soccer',
        event='full_run',
        entity_id='auto',
        team_id='auto',
        market_id=None,
        bankroll=1000.0,
        min_edge=0.02,
    )

    print(json.dumps(result, indent=4))

