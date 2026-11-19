"""Real Moomoo OpenD one-minute source; no synthetic fallback."""
from __future__ import annotations

import pandas as pd


class MoomooOpenDSource:
    def __init__(self, host: str = "127.0.0.1", port: int = 11111):
        self.host = host
        self.port = int(port)

    def fetch_1m(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        try:
            from moomoo import AuType, KLType, KL_FIELD, OpenQuoteContext, RET_OK
        except ImportError as exc:
            raise RuntimeError("install the runtime extra to use Moomoo OpenD") from exc
        quote = OpenQuoteContext(host=self.host, port=self.port)
        frames, page_key = [], None
        try:
            while True:
                ret, data, page_key = quote.request_history_kline(
                    code=symbol, start=start, end=end, ktype=KLType.K_1M,
                    autype=AuType.QFQ, fields=[KL_FIELD.ALL], max_count=1000,
                    page_req_key=page_key, extended_time=False,
                )
                if ret != RET_OK:
                    raise RuntimeError(f"Moomoo candle request failed: {data}")
                if data is not None and not data.empty:
                    frames.append(data.copy())
                if page_key is None:
                    break
        finally:
            quote.close()
        if not frames:
            raise RuntimeError("Moomoo returned no candles")
        frame = pd.concat(frames, ignore_index=True)
        frame["time_key"] = pd.to_datetime(frame["time_key"], errors="raise")
        frame = frame.sort_values("time_key").drop_duplicates("time_key").set_index("time_key")
        required = ["open", "high", "low", "close"]
        frame = frame.dropna(subset=required)
        if frame.empty:
            raise RuntimeError("Moomoo returned no valid OHLC candles")
        return frame
