import sqlite3
import time
from pathlib import Path
from threading import Lock

class oxiusCache:
    def __init__(self, db_path="Cache/oxius.db", ttl=300):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.ttl = ttl
        self.lock = Lock()
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                url TEXT PRIMARY KEY,
                response TEXT,
                expiry INTEGER
            )
        """)
        self.conn.commit()

    def get(self, url):
        with self.lock:
            now = int(time.time())
            row = self.conn.execute(
                "SELECT response FROM cache WHERE url=? AND expiry > ?",
                (url, now)
            ).fetchone()
            return row[0] if row else None

    def set(self, url, response):
        with self.lock:
            expiry = int(time.time()) + self.ttl
            self.conn.execute(
                "REPLACE INTO cache (url, response, expiry) VALUES (?, ?, ?)",
                (url, response, expiry)
            )
            self.conn.commit()

    def delete(self, url):
        with self.lock:
            self.conn.execute("DELETE FROM cache WHERE url=?", (url,))
            self.conn.commit()

    def clear(self):
        with self.lock:
            self.conn.execute("DELETE FROM cache")
            self.conn.commit()

    def cleanup(self):
        with self.lock:
            now = int(time.time())
            self.conn.execute("DELETE FROM cache WHERE expiry <= ?", (now,))
            self.conn.commit()

    def close(self):
        with self.lock:
            self.conn.close()
