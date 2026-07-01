from typing import List

def brier_score(predictions: List[float], outcomes: List[int]) -> float:
    if len(predictions) != len(outcomes):
        raise ValueError("Predictions y outcomes deben tener la misma longitud.")
    n = len(predictions)
    return sum((p - o) ** 2 for p, o in zip(predictions, outcomes)) / n

def accuracy(predictions: List[float], outcomes: List[int], threshold: float = 0.5) -> float:
    if len(predictions) != len(outcomes):
        raise ValueError("Predictions y outcomes deben tener la misma longitud.")
    decisions = [1 if p >= threshold else 0 for p in predictions]
    correct = sum(1 for d, o in zip(decisions, outcomes) if d == o)
    return correct / len(outcomes)

