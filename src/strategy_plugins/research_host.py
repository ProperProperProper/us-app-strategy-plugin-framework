"""Trusted candidate evaluation and promotion boundary."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .us_app_evaluator import USAppEvaluator
from .us_app_plugin import USAppStrategyPlugin


class PluginResearchHost:
    """Evaluate real candidates; plugins never decide their own promotion."""

    def __init__(self, plugin: USAppStrategyPlugin, runtime_artifact: str | Path):
        self.plugin = plugin
        self.evaluator = USAppEvaluator(Path(plugin.module.__file__).resolve().parents[1], plugin)
        self.runtime_artifact = Path(runtime_artifact)

    def evaluate(self, candles, candidate: dict[str, Any] | None = None) -> dict[str, Any]:
        params = {**self.plugin.baseline, **(candidate or {})}
        self.plugin.validate_config(params)
        baseline = self.evaluator.replay(candles, [self.plugin.baseline])
        result = self.evaluator.replay(candles, [params])
        baseline_stats = baseline.get("aggregate", {})
        candidate_stats = result.get("aggregate", {})
        reasons = []
        if result.get("status") != "OK":
            reasons.append("candidate_replay_not_ok")
        if int(candidate_stats.get("trades", 0)) < 3:
            reasons.append("blind_replay_trades_below_minimum")
        if float(candidate_stats.get("total_return_pct", 0)) <= float(baseline_stats.get("total_return_pct", 0)):
            reasons.append("blind_replay_return_not_above_baseline")
        if float(candidate_stats.get("max_drawdown_pct", 0)) < float(baseline_stats.get("max_drawdown_pct", 0)) - 1.0:
            reasons.append("drawdown_degradation_above_one_percentage_point")
        return {
            "plugin": {"name": self.plugin.manifest.name, "version": self.plugin.manifest.version},
            "params": params,
            "baseline": baseline_stats,
            "candidate": candidate_stats,
            "replay": result,
            "promotable": not reasons,
            "reasons": reasons,
        }

    def promote(self, evidence: dict[str, Any]) -> dict[str, Any]:
        if not evidence.get("promotable"):
            raise ValueError(f"candidate is not promotable: {evidence.get('reasons', [])}")
        payload = {
            "plugin": evidence["plugin"],
            "params": evidence["params"],
            "interval": 10,
            "mode": "SIMULATE",
            "promotion": {
                "baseline": evidence["baseline"],
                "candidate": evidence["candidate"],
                "replay_protocol": "first_21_complete_sessions_then_one_continuous_unseen_replay",
            },
        }
        self.runtime_artifact.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=self.runtime_artifact.name + ".", dir=self.runtime_artifact.parent)
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")
            os.replace(temporary, self.runtime_artifact)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return payload
