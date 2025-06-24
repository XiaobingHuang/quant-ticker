import os
import logging
from clickhouse_driver import Client
import asyncio

class ClickHouseWriter:
    def __init__(
        self,
        host=None,
        port=9000,
        database="market",
        table="coinbase_ticks",
        batch_size=100,
        user="default",
        password=""
    ):
        # Fallback order: arg > env var > inside Docker use service name 'clickhouse' > else localhost
        self.host = (
            host or
            os.getenv("CLICKHOUSE_HOST") or
            ("clickhouse" if os.getenv("INSIDE_DOCKER") else "localhost")
        )
        self.port = port
        self.database = database
        self.table = table
        self.batch_size = batch_size

        logging.debug(f"Connecting to ClickHouse at {self.host}:{self.port}")
        self.client = Client(
            host=self.host,
            port=self.port,
            user=user,
            password=password,
            database=database
        )
        self.buffer = []
        self._init_db()

    def _init_db(self):
        self.client.execute(f"CREATE DATABASE IF NOT EXISTS {self.database};")
        self.client.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.database}.{self.table} (
                timestamp DateTime64(3),
                symbol String,
                price Float64,
                volume Float64
            ) ENGINE = MergeTree()
            ORDER BY (symbol, timestamp);
        """)

    async def write(self, tick):
        self.buffer.append((
            tick["timestamp"],
            tick["symbol"],
            tick["price"],
            tick["volume"]
        ))
        if len(self.buffer) >= self.batch_size:
            self.flush()

    def flush(self):
        if self.buffer:
            self.client.execute(
                f"INSERT INTO {self.database}.{self.table} (timestamp, symbol, price, volume) VALUES",
                self.buffer
            )
            self.buffer = []

    def close(self):
        self.flush()
