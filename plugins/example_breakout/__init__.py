"""Reference strategy plugin with no broker or account integration."""
from strategy_plugins.contracts import PluginManifest


class ExampleBreakout:
    manifest = PluginManifest(
        name="example-breakout", version="0.1.0", kind="strategy",
        capabilities=("entry_signal", "exit_signal"),
        supported_intervals=(10, 20, 30, 40, 50, 60, 70),
    )

    def validate_config(self, config):
        lookback = int(config.get("lookback", 20))
        if lookback < 2 or lookback > 500:
            raise ValueError("lookback must be between 2 and 500")

    def entry_signal(self, features, config):
        self.validate_config(config)
        lookback = int(config.get("lookback", 20))
        return features["close"] > features["high"].shift(1).rolling(lookback).max()

    def exit_signal(self, features, position, config):
        self.validate_config(config)
        return features["close"] < features["ema_slow"]
