"""Real US.APP strategy plugin backed by the existing deterministic lab."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Mapping

from .contracts import PluginManifest


class USAppStrategyPlugin:
    manifest = PluginManifest(
        name="us-app-donchian-ema", version="lab-source", kind="strategy",
        capabilities=("causal_features", "entry_signal", "exit_signal", "blind_replay"),
        supported_intervals=(10, 20, 30, 40, 50, 60, 70), trusted=True,
    )

    def __init__(self, lab_root: str | Path):
        source = Path(lab_root).resolve() / "scripts" / "strategy_57pct.py"
        if not source.exists():
            raise FileNotFoundError(f"US.APP strategy source not found: {source}")
        spec = importlib.util.spec_from_file_location("us_app_strategy_plugin", source)
        if spec is None or spec.loader is None:
            raise ImportError(f"could not load strategy source: {source}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        self.module = module

    @property
    def baseline(self) -> dict[str, Any]:
        return dict(self.module.BASELINE)

    def validate_config(self, config: Mapping[str, Any]) -> None:
        params = {**self.baseline, **dict(config)}
        if int(params["lookback"]) < 2 or int(params["slow"]) <= int(params["fast"]):
            raise ValueError("US.APP lookback and EMA parameters are invalid")

    def features(self, candles, config: Mapping[str, Any]):
        self.validate_config(config)
        return self.module.add_features(candles, {**self.baseline, **dict(config)})

    def entry_signal(self, features, config: Mapping[str, Any]):
        self.validate_config(config)
        return features["entry_signal"].fillna(False)

    def exit_signal(self, features, position: Mapping[str, Any], config: Mapping[str, Any]):
        self.validate_config(config)
        return features["exit_signal"].fillna(False)
