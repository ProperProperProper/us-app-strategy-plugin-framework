"""Validated SQLite candle storage for real source data."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd

# Interval 1 is the immutable broker-source series; 2..21 are local derived bars.
RESEARCH_INTERVALS = tuple(range(1, 22))
MIN_CANDLE_DATE = pd.Timestamp("2026-01-01")


class CandleStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path, timeout=30)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=30000")
        db.execute("""CREATE TABLE IF NOT EXISTS candles (
            symbol TEXT NOT NULL, interval_minutes INTEGER NOT NULL,
            time_key TEXT NOT NULL, open REAL NOT NULL, high REAL NOT NULL,
            low REAL NOT NULL, close REAL NOT NULL, volume REAL,
            turnover REAL, source TEXT NOT NULL,
            PRIMARY KEY(symbol, interval_minutes, time_key))""")
        db.execute("DELETE FROM candles WHERE time_key < '2026-01-01T00:00:00'")
        placeholders = ",".join("?" for _ in RESEARCH_INTERVALS)
        db.execute(f"DELETE FROM candles WHERE interval_minutes NOT IN ({placeholders})", RESEARCH_INTERVALS)
        db.commit()
        return db

    def save(self, frame: pd.DataFrame, symbol: str, interval: int = 1, source: str = "moomoo_opend") -> int:
        if interval not in RESEARCH_INTERVALS:
            raise ValueError(f"interval must be one of {RESEARCH_INTERVALS}")
        required = {"open", "high", "low", "close"}
        if not required.issubset(frame.columns):
            raise ValueError(f"missing candle columns: {sorted(required - set(frame.columns))}")
        rows = []
        for stamp, row in frame.sort_index().iterrows():
            stamp = pd.Timestamp(stamp)
            if stamp.tzinfo is not None:
                stamp = stamp.tz_localize(None)
            values = [float(row[name]) for name in ("open", "high", "low", "close")]
            volume = float(row["volume"]) if "volume" in row and pd.notna(row["volume"]) else None
            if stamp < MIN_CANDLE_DATE or any(value <= 0 for value in values):
                continue
            open_, high, low, close = values
            if high < max(open_, close) or low > min(open_, close) or high < low or (volume is not None and volume < 0):
                raise ValueError(f"malformed OHLCV candle at {stamp}")
            rows.append((symbol, interval, stamp.isoformat(), open_, high, low, close, volume, row.get("turnover"), source))
        with self.connect() as db:
            db.executemany("""INSERT OR IGNORE INTO candles
                (symbol, interval_minutes, time_key, open, high, low, close, volume, turnover, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", rows)
            db.commit()
        return len(rows)

    def load(self, symbol: str, interval: int = 1) -> pd.DataFrame:
        if interval not in RESEARCH_INTERVALS:
            raise ValueError(f"interval must be one of {RESEARCH_INTERVALS}")
        with self.connect() as db:
            frame = pd.read_sql_query(
                "SELECT time_key,open,high,low,close,volume,turnover FROM candles WHERE symbol=? AND interval_minutes=? ORDER BY time_key",
                db, params=(symbol, interval), parse_dates=["time_key"],
            )
        return frame.set_index("time_key") if not frame.empty else frame
