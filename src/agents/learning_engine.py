from typing import List, Dict

class MercuryLearningEngine:
    """
    Motor de aprendizaje basado en datos reales.
    """

    def evaluate_predictions(self, predictions: List[Dict], outcomes: Dict[str, bool]):
        """
        predictions: [{"id": str, "prob": float}]
        outcomes: {id: True/False}
        """

        if not predictions:
            return {"accuracy": 0.0, "brier_score": 0.0, "count": 0}

        correct = 0
        brier_sum = 0.0
        n = 0

        for pred in predictions:
            mid = pred["id"]
            prob = pred["prob"]
            outcome = outcomes.get(mid, False)

            y = 1.0 if outcome else 0.0
            brier_sum += (prob - y) ** 2
            n += 1

            if (prob >= 0.5 and outcome) or (prob < 0.5 and not outcome):
                correct += 1

        return {
            "accuracy": correct / n,
            "brier_score": brier_sum / n,
            "count": n
        }

