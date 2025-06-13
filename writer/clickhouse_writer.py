from clickhouse_driver import Client
import asyncio

class ClickHouseWriter:
    def __init__(
        self,
        host="localhost",  # Use this if running Python outside Docker on macOS
        port=9000,
        database="default",  # ❗ this database doesn't exist yet
        table="coinbase_ticks",
        batch_size=100,
        user="default",
        password=""
    ):
        self.client = Client(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.table = table
        self.batch_size = batch_size
        self.buffer = []

        self._init_db()

    def _init_db(self):
        self.client.execute(f"""
            CREATE DATABASE IF NOT EXISTS market;
        """)

        self.client.execute(f"""
            CREATE TABLE IF NOT EXISTS market.{self.table} (
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
                f"INSERT INTO market.{self.table} (timestamp, symbol, price, volume) VALUES",
                self.buffer
            )
            self.buffer = []

    def close(self):
        self.flush()
