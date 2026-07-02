import json

# Edge estimator
# Uses market price and internal probability to compute expected value and edge

def compute_edge(p_true, market_price):
    # p_true: internal probability estimate (0.0 - 1.0)
    # market_price: YES price in dollars (0.0 - 1.0)
    profit_if_win = 1.0 - market_price
    cost_if_lose = market_price

    ev = p_true * profit_if_win - (1.0 - p_true) * cost_if_lose
    edge = p_true - market_price

    return {
        "p_true": p_true,
        "market_price": market_price,
        "expected_value": ev,
        "edge": edge
    }
