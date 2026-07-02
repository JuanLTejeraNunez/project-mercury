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
