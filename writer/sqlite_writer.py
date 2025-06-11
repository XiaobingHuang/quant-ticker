# writer/sqlite_writer.py

import sqlite3
import os
from config import OUTPUT_DIR, SQLITE_DB_NAME, SQLITE_TABLE_NAME
import asyncio

class SQLiteWriter:
    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.db_path = os.path.join(OUTPUT_DIR, SQLITE_DB_NAME)
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {SQLITE_TABLE_NAME} (
                    timestamp TEXT,
                    symbol TEXT,
                    price REAL,
                    volume REAL
                );
            """)

    async def write(self, data):
        with self.conn:
            self.conn.execute(f"""
                INSERT INTO {SQLITE_TABLE_NAME} (timestamp, symbol, price, volume)
                VALUES (?, ?, ?, ?)
            """, (data["timestamp"], data["symbol"], data["price"], data["volume"]))
