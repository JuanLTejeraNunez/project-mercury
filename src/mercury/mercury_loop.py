import time
import logging
import json
from pathlib import Path

from providers.market_router import MarketRouter
from agents.analysis_agent import evaluate_and_place_bet_from_market
from core.circuit_breaker import CircuitBreaker
from database.sqlite_manager import SQLiteManager

class MercuryLoop:
    def __init__(self, config_path="config/mercury_config.json"):
        self.config = json.loads(Path(config_path).read_text())
        self.db = SQLiteManager(self.config["database"]["path"])
        self.cb = CircuitBreaker(
            max_drawdown_pct=self.config["circuit_breaker"]["max_drawdown_pct"],
            max_consecutive_losses=self.config["circuit_breaker"]["max_consecutive_losses"],
            min_bankroll=self.config["circuit_breaker"]["min_bankroll"]
        )
        self.router = MarketRouter(config_path=config_path)
        self.bankroll = 1000.0

    def setup(self):
        logging.basicConfig(
            filename=self.config["logs"]["loop_log"],
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.db.connect()
        self.cb.initialize(self.bankroll)
        logging.info("[MercuryLoop] Setup completado.")

    def run_cycle(self, sport: str = "baseball"):
        markets = self.router.fetch_markets(sport)
        logging.info(f"[MercuryLoop] Recibidos {len(markets)} mercados para sport={sport}.")

        if not markets:
            logging.warning("[MercuryLoop] No hay mercados disponibles en este ciclo.")
            return False

        # Tomar el primer mercado como ejemplo
        market = markets[0]
        opp = evaluate_and_place_bet_from_market(market, bankroll=self.bankroll)

        self.db.insert_opportunity(opp)

        if opp["decision"] == "place_bet":
            self.bankroll -= opp["stake"]

        stop = self.cb.register_result(
            won=(opp["edge"] > 0),
            bankroll=self.bankroll
        )

        return stop

    def start(self, sport: str = "baseball"):
        self.setup()
        logging.info(f"[MercuryLoop] Iniciando loop para sport={sport}...")

        while True:
            stop = self.run_cycle(sport=sport)
            if stop:
                logging.warning("[MercuryLoop] Circuit breaker activado. Deteniendo loop.")
                break

            time.sleep(self.config["mercury_loop"]["poll_interval_seconds"])

        self.db.close()
        logging.info("[MercuryLoop] Loop finalizado, conexión a DB cerrada.")
