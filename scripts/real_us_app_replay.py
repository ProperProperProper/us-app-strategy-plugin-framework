#!/usr/bin/env python3
"""Fetch real US.APP candles and run the real deterministic replay."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from strategy_plugins import CandleStore, MoomooOpenDSource, USAppEvaluator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab-root", type=Path, required=True, help="path to us-app-paper-strategy-lab")
    parser.add_argument("--db", type=Path, default=Path("quant_dashboard.sqlite3"))
    parser.add_argument("--symbol", default="US.APP")
    parser.add_argument("--start", required=True, help="inclusive timestamp")
    parser.add_argument("--end", required=True, help="inclusive timestamp")
    parser.add_argument("--fetch", action="store_true", help="fetch real candles from local Moomoo OpenD")
    args = parser.parse_args()

    store = CandleStore(args.db)
    if args.fetch:
        frame = MoomooOpenDSource().fetch_10m(args.symbol, args.start, args.end)
        store.save(frame, args.symbol, 10)
    frame = store.load(args.symbol, 10)
    if frame.empty:
        raise RuntimeError("no real candles available; use --fetch with Moomoo OpenD running")
    result = USAppEvaluator(args.lab_root).replay(frame)
    print(json.dumps({"symbol": args.symbol, "rows": len(frame), "replay": result}, default=str, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
