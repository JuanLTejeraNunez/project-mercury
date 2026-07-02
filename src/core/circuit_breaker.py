import logging

class CircuitBreaker:
    def __init__(self, max_drawdown_pct=0.25, max_consecutive_losses=5, min_bankroll=100):
        self.max_drawdown_pct = max_drawdown_pct
        self.max_consecutive_losses = max_consecutive_losses
        self.min_bankroll = min_bankroll
        self.starting_bankroll = None
        self.consecutive_losses = 0

    def initialize(self, bankroll):
        self.starting_bankroll = bankroll
        self.consecutive_losses = 0

    def register_result(self, won: bool, bankroll: float):
        if not won:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

        drawdown = 1 - (bankroll / self.starting_bankroll)

        if drawdown >= self.max_drawdown_pct:
            logging.warning(f"[CircuitBreaker] Drawdown exceeded: {drawdown:.2%}")
            return True

        if self.consecutive_losses >= self.max_consecutive_losses:
            logging.warning(f"[CircuitBreaker] Too many consecutive losses: {self.consecutive_losses}")
            return True

        if bankroll <= self.min_bankroll:
            logging.warning(f"[CircuitBreaker] Bankroll too low: {bankroll}")
            return True

        return False
