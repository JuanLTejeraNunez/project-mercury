<#
    create_mercury_modules.ps1
    Script único para crear todos los módulos:

      - config/mercury_config.json
      - logs/mercury_loop.log
      - src/core/circuit_breaker.py
      - src/database/sqlite_manager.py
      - src/mercury/mercury_loop.py

    Si la carpeta no existe, se crea.
    Si el archivo existe, se sobrescribe.
#>

# Detectar raíz del proyecto
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
Write-Host "Raiz detectada: $Root"

# ============================
# Crear carpetas necesarias
# ============================

$folders = @(
    "config",
    "logs",
    "src/core",
    "src/database",
    "src/mercury"
)

foreach ($f in $folders) {
    $path = Join-Path $Root $f
    if (-not (Test-Path $path)) {
        Write-Host "Creando carpeta: $f"
        New-Item -ItemType Directory -Path $path | Out-Null
    } else {
        Write-Host "Carpeta ya existe: $f"
    }
}

# ============================
# Crear config/mercury_config.json
# ============================

$configPath = "config/mercury_config.json"
Write-Host "Creando $configPath"

@"
{
  "version": "1.0",
  "database": {
    "path": "data/memory.sqlite",
    "timeout": 5
  },
  "logs": {
    "loop_log": "logs/mercury_loop.log",
    "agent_log": "logs/agent_20260701.log"
  },
  "circuit_breaker": {
    "max_drawdown_pct": 0.25,
    "max_consecutive_losses": 5,
    "min_bankroll": 100
  },
  "mercury_loop": {
    "poll_interval_seconds": 30,
    "max_opportunities_per_cycle": 10,
    "min_edge_threshold": 0.01
  },
  "providers": {
    "polymarket": {
      "enabled": true,
      "api_url": "https://clob.polymarket.com/markets"
    },
    "kalshi": {
      "enabled": true,
      "api_url": "https://api.kalshi.com/v1/markets"
    }
  }
}
"@ | Set-Content $configPath

# ============================
# Crear logs/mercury_loop.log
# ============================

$logPath = "logs/mercury_loop.log"
Write-Host "Creando $logPath"
"" | Set-Content $logPath

# ============================
# Crear src/core/circuit_breaker.py
# ============================

$circuitPath = "src/core/circuit_breaker.py"
Write-Host "Creando $circuitPath"

@"
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
"@ | Set-Content $circuitPath

# ============================
# Crear src/database/sqlite_manager.py
# ============================

$dbPath = "src/database/sqlite_manager.py"
Write-Host "Creando $dbPath"

@"
import sqlite3
import logging
from pathlib import Path

class SQLiteManager:
    def __init__(self, db_path="data/memory.sqlite"):
        self.db_path = Path(db_path)
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sport TEXT,
                event TEXT,
                entity_id TEXT,
                team_id TEXT,
                p_internal REAL,
                p_market REAL,
                edge REAL,
                stake REAL,
                decision TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_opportunity(self, opp: dict):
        query = """
            INSERT INTO opportunities
            (sport, event, entity_id, team_id, p_internal, p_market, edge, stake, decision)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            opp["sport"],
            opp["event"],
            opp["entity_id"],
            opp["team_id"],
            opp["p_internal"],
            opp["p_market"],
            opp["edge"],
            opp["stake"],
            opp["decision"]
        )
        self.conn.execute(query, values)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
"@ | Set-Content $dbPath

# ============================
# Crear src/mercury/mercury_loop.py
# ============================

$loopPath = "src/mercury/mercury_loop.py"
Write-Host "Creando $loopPath"

@"
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
"@ | Set-Content $loopPath

# ============================
# Git commit + push
# ============================

Write-Host "Realizando commit y push..."

git add .
git commit -m "Added Mercury modules: config, logs, circuit breaker, sqlite manager, mercury loop"
git push

Write-Host "Proceso completado."
