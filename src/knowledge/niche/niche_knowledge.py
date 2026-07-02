from .niche_api_mma import get_mma_stats
from .niche_api_boxing import get_boxing_stats
from .niche_api_cricket import get_cricket_stats
from .niche_api_rugby import get_rugby_stats

def compute_internal_probability(event, entity_id, team_id=None):
    if event == "mma_finish":
        return get_mma_stats(entity_id)["event_rate"]
    if event == "boxing_ko":
        return get_boxing_stats(entity_id)["event_rate"]
    if event == "cricket_runs":
        return get_cricket_stats(entity_id, team_id)["event_rate"]
    if event == "rugby_try":
        return get_rugby_stats(entity_id, team_id)["event_rate"]
    return 0.1


