import time
import logging
import json
from pathlib import Path

from core.circuit_breaker import CircuitBreaker
from database.sqlite_manager import SQLiteManager
from agents.analysis_agent import evaluate_and_place_bet

class MercuryLoop:
    def __init__(self, config_path="config/mercury_config.json"):
        self.config = json.loads(Path(config_path).read_text())
        self.db = SQLiteManager(self.config["database"]["path"])
        self.cb = CircuitBreaker(
            max_drawdown_pct=self.config["circuit_breaker"]["max_drawdown_pct"],
            max_consecutive_losses=self.config["circuit_breaker"]["max_consecutive_losses"],
            min_bankroll=self.config["circuit_breaker"]["min_bankroll"]
        )
        self.bankroll = 1000.0

    def setup(self):
        logging.basicConfig(
            filename=self.config["logs"]["loop_log"],
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.db.connect()
        self.cb.initialize(self.bankroll)

    def run_cycle(self):
        opp = evaluate_and_place_bet(
            sport="baseball",
            event="hit_today",
            entity_id="player_123",
            team_id="team_abc",
            market_id="low_example",
            bankroll=self.bankroll
        )

        self.db.insert_opportunity(opp)

        if opp["decision"] == "place_bet":
            self.bankroll -= opp["stake"]

        stop = self.cb.register_result(
            won=(opp["edge"] > 0),
            bankroll=self.bankroll
        )

        return stop

    def start(self):
        self.setup()
        logging.info("[MercuryLoop] Starting loop...")

        while True:
            stop = self.run_cycle()
            if stop:
                logging.warning("[MercuryLoop] Circuit breaker triggered. Stopping loop.")
                break

            time.sleep(self.config["mercury_loop"]["poll_interval_seconds"])

        self.db.close()
