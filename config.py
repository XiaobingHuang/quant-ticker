# config.py

# Symbols to track (e.g., crypto or stock tickers)
SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
]

# Data interval (seconds between fetches or candle period)
FETCH_INTERVAL = 1  # in seconds
AGGREGATION_INTERVAL = "1min"  # used for OHLCV aggregation

# Output settings
OUTPUT_MODE = "csv"  # options: "csv", "sqlite"
OUTPUT_DIR = "data/"  # where to save logs or database

# SQLite file name
SQLITE_DB_NAME = "market_data.db"
SQLITE_TABLE_NAME = "tick_data"

# CSV settings
CSV_FILENAME = "tick_data.csv"
CSV_HEADER = ["timestamp", "symbol", "price", "volume"]

# API keys (if using authenticated APIs)
IEX_API_KEY = ""  # optional
BINANCE_REST_ENDPOINT = "https://api.binance.com/api/v3"
BINANCE_WS_ENDPOINT = "wss://stream.binance.com:9443"

# Reconnection settings
MAX_RETRIES = 5
RETRY_DELAY = 3  # seconds
