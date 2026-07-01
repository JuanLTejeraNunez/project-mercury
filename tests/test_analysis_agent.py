from src.agents.analysis_agent import MercuryAnalysisAgent
from src.utils.metrics import brier_score, accuracy

def test_bayes_update_basic():
    agent = MercuryAnalysisAgent()
    posterior = agent.bayes_update(prior=0.5, likelihood=0.8, evidence=0.6)
    assert 0.0 <= posterior <= 1.0

def test_implied_probability_from_price():
    agent = MercuryAnalysisAgent()
    prob = agent.implied_probability_from_price(0.7)
    assert prob == 0.7

def test_brier_score_and_accuracy():
    preds = [0.8, 0.3, 0.6, 0.9]
    outcomes = [1, 0, 1, 1]
    score = brier_score(preds, outcomes)
    acc = accuracy(preds, outcomes)
    assert 0.0 <= score <= 1.0
    assert 0.0 <= acc <= 1.0

