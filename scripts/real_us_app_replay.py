#!/usr/bin/env python3
"""Fetch real US.APP candles and run the real deterministic replay."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from strategy_plugins import CandleStore, MoomooOpenDSource, PluginRegistry, PluginResearchHost, USAppStrategyPlugin


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab-root", type=Path, required=True, help="path to us-app-paper-strategy-lab")
    parser.add_argument("--db", type=Path, default=Path("quant_dashboard.sqlite3"))
    parser.add_argument("--symbol", default="US.APP")
    parser.add_argument("--start", required=True, help="inclusive timestamp")
    parser.add_argument("--end", required=True, help="inclusive timestamp")
    parser.add_argument("--fetch", action="store_true", help="fetch real candles from local Moomoo OpenD")
    parser.add_argument("--candidate-json", type=Path, help="JSON object containing a bounded candidate parameter mutation")
    parser.add_argument("--promote-artifact", type=Path, help="existing paper-bot runtime artifact to update only after the gate passes")
    args = parser.parse_args()

    store = CandleStore(args.db)
    if args.fetch:
        frame = MoomooOpenDSource().fetch_10m(args.symbol, args.start, args.end)
        store.save(frame, args.symbol, 10)
    frame = store.load(args.symbol, 10)
    if frame.empty:
        raise RuntimeError("no real candles available; use --fetch with Moomoo OpenD running")
    plugin = USAppStrategyPlugin(args.lab_root)
    registry = PluginRegistry()
    registry.register(plugin)
    candidate = json.loads(args.candidate_json.read_text()) if args.candidate_json else None
    host = PluginResearchHost(plugin, args.promote_artifact or Path("plugin_runtime.json"))
    evidence = host.evaluate(frame, candidate)
    promoted = None
    if args.promote_artifact:
        if not evidence["promotable"]:
            raise RuntimeError(f"candidate rejected; artifact was not changed: {evidence['reasons']}")
        promoted = host.promote(evidence)
    print(json.dumps({"symbol": args.symbol, "rows": len(frame), "evidence": evidence, "promoted": promoted}, default=str, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
