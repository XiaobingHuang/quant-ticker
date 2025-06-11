# writer/csv_writer.py

import csv
import os
from config import OUTPUT_DIR, CSV_FILENAME, CSV_HEADER
import asyncio

class CSVWriter:
    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.file_path = os.path.join(OUTPUT_DIR, CSV_FILENAME)
        self._ensure_header()

    def _ensure_header(self):
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            with open(self.file_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADER)

    async def write(self, data):
        with open(self.file_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                data["timestamp"],
                data["symbol"],
                data["price"],
                data["volume"]
            ])
