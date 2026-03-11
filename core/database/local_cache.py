"""SQLite Local Cache - Render.com Free Tier"""

import sqlite3
import json
from typing import Optional, Dict


class ThreatCache:
    """SQLite-based threat cache for free tier deployment"""

    def __init__(self, db_path: str = "chronoscope.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS threats (
                ip TEXT PRIMARY KEY,
                data TEXT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def get(self, ip: str) -> Optional[Dict]:
        cur = self.conn.execute("SELECT data FROM threats WHERE ip = ?", (ip,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None

    def store(self, ip: str, data: Dict):
        self.conn.execute(
            "INSERT OR REPLACE INTO threats (ip, data) VALUES (?, ?)",
            (ip, json.dumps(data))
        )
        self.conn.commit()

    def stats(self) -> Dict:
        cur = self.conn.execute("SELECT COUNT(*) FROM threats")
        return {"total_ips": cur.fetchone()[0], "database": "sqlite"}
