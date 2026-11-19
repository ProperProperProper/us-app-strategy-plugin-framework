"""Versioned plugin contracts with no broker or model permissions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    kind: str
    api_version: str = "1"
    capabilities: tuple[str, ...] = ()
    supported_intervals: tuple[int, ...] = (10,)
    trusted: bool = False


class IndicatorPlugin(Protocol):
    manifest: PluginManifest
    def calculate(self, candles: Any, config: Mapping[str, Any]) -> Any: ...


class StrategyPlugin(Protocol):
    manifest: PluginManifest
    def validate_config(self, config: Mapping[str, Any]) -> None: ...
    def entry_signal(self, features: Any, config: Mapping[str, Any]) -> Any: ...
    def exit_signal(self, features: Any, position: Mapping[str, Any], config: Mapping[str, Any]) -> Any: ...


class ProposalProviderPlugin(Protocol):
    manifest: PluginManifest
    def propose(self, brief: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]: ...


class ExecutionModelPlugin(Protocol):
    manifest: PluginManifest
    def estimate_fill(self, side: str, price: float, quantity: int, context: Mapping[str, Any]) -> float: ...


@dataclass(frozen=True)
class PluginRecord:
    manifest: PluginManifest
    plugin: Any = field(repr=False)
