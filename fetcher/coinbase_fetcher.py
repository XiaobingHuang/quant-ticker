# fetcher/coinbase_fetcher.py

import asyncio
import json
import logging
import websockets
from datetime import datetime

from config import COINBASE_WS_ENDPOINT, COINBASE_SYMBOLS, FETCH_INTERVAL

logger = logging.getLogger(__name__)

async def fetch_coinbase_stream(symbols, writer, shutdown_flag):
    subscribe_msg = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": symbols}]
    }

    try:
        async with websockets.connect(COINBASE_WS_ENDPOINT) as ws:
            await ws.send(json.dumps(subscribe_msg))
            logger.info(f"Subscribed to Coinbase ticker for {symbols}")

            while not shutdown_flag.is_set():
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=FETCH_INTERVAL + 1)
                    data = json.loads(msg)
                    print(data)

                    if data.get("type") == "ticker":
                        tick = {
                            "timestamp": datetime.utcnow().isoformat(),
                            "symbol": data["product_id"],
                            "price": float(data["price"]),
                            "volume": float(data.get("last_size", 0.0))
                        }
                        await writer.write(tick)

                except asyncio.TimeoutError:
                    logger.warning("Timeout — waiting for data...")
                except Exception as e:
                    logger.error(f"Coinbase stream error: {e}")
                    await asyncio.sleep(1)
    except Exception as e:
        logger.exception(f"WebSocket connection failed: {e}")
