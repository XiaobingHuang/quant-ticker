# fetcher/binance_fetcher.py

import asyncio
import json
import logging
import websockets
from datetime import datetime

from config import FETCH_INTERVAL

logger = logging.getLogger(__name__)

async def fetch_binance_stream(symbols, writer, shutdown_flag):
    stream = "/".join([f"{symbol.lower()}@trade" for symbol in symbols])
    url = f"wss://stream.binance.com:9443/stream?streams={stream}"

    async with websockets.connect(url) as websocket:
        logger.info(f"Connected to Binance WebSocket for: {symbols}")
        while not shutdown_flag.is_set():
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=FETCH_INTERVAL + 1)
                data = json.loads(message)

                tick = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "symbol": data["data"]["s"],
                    "price": float(data["data"]["p"]),
                    "volume": float(data["data"]["q"])
                }

                await writer.write(tick)
            except asyncio.TimeoutError:
                logger.warning("WebSocket timeout — retrying...")
            except Exception as e:
                logger.error(f"Error fetching data: {e}")
