"""Trusted contracts for safety-bounded quantitative research plugins."""

from .contracts import ExecutionModelPlugin, IndicatorPlugin, PluginManifest, ProposalProviderPlugin, StrategyPlugin
from .registry import PluginRegistry
from .sqlite_candles import CandleStore
from .moomoo_source import MoomooOpenDSource
from .us_app_evaluator import USAppEvaluator
from .moomoo_simulate import MoomooSimulateExecutor
from .us_app_plugin import USAppStrategyPlugin
from .research_host import PluginResearchHost
from .artifacts import PaperRuntimeArtifact, PluginReference, PromotionEvidence

__all__ = ["ExecutionModelPlugin", "IndicatorPlugin", "PluginManifest", "ProposalProviderPlugin", "StrategyPlugin", "PluginRegistry", "CandleStore", "MoomooOpenDSource", "USAppEvaluator", "MoomooSimulateExecutor", "USAppStrategyPlugin", "PluginResearchHost", "PaperRuntimeArtifact", "PluginReference", "PromotionEvidence"]
