import math

# Kelly bet sizing for binary markets
# Uses fractional Kelly to reduce variance

def kelly_fraction(p_true, market_price, fraction=0.5):
    # p_true: internal probability estimate
    # market_price: YES price (0.0 - 1.0)
    # fraction: 0.25, 0.5, etc. for fractional Kelly

    b = (1.0 - market_price) / market_price
    q = 1.0 - p_true

    full_kelly = (p_true * b - q) / b

    if full_kelly <= 0.0:
        return 0.0

    return full_kelly * fraction
