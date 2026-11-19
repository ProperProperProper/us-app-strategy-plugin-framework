"""Adapter to the real US.APP deterministic evaluator."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pandas as pd


class USAppEvaluator:
    def __init__(self, lab_root: str | Path):
        root = Path(lab_root).resolve()
        source = root / "scripts" / "strategy_57pct.py"
        if not source.exists():
            raise FileNotFoundError(f"US.APP evaluator not found: {source}")
        spec = importlib.util.spec_from_file_location("us_app_strategy_plugin_runtime", source)
        if spec is None or spec.loader is None:
            raise ImportError(f"could not load evaluator: {source}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        self.module = module

    def replay(self, candles: pd.DataFrame, candidates: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        """Run the real first-21-session/continuous-unseen replay."""
        candidates = candidates or [dict(self.module.BASELINE)]
        return self.module.blind_session_walk_forward(candles, candidates, min_train_sessions=21)

    @property
    def baseline(self) -> dict[str, Any]:
        return dict(self.module.BASELINE)
