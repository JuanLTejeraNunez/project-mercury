# REMOVED: import MercurySimulationEngine (simulation removed)

def test_simulate_binary_events():
    engine = MercurySimulationEngine()
    probs = [0.7, 0.3]
    outcomes = engine.simulate_binary_events(probs, trials=10)
    assert len(outcomes) == 20
    assert all(o in (0, 1) for o in outcomes)

def test_simulate_pnl():
    engine = MercurySimulationEngine()
    probs = [0.6, 0.4, 0.7]
    result = engine.simulate_pnl(probs, stake=10.0)
    assert "pnl" in result
    assert "win_rate" in result
    assert "trades" in result
    assert result["trades"] == len(probs)


