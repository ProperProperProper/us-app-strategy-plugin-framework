import pandas as pd
from example_breakout import ExampleBreakout


def test_example_strategy_is_signal_only_and_causal():
    frame = pd.DataFrame({"close": [1, 2, 3, 4], "high": [1, 2, 3, 4], "ema_slow": [1, 1, 2, 3]})
    plugin = ExampleBreakout()
    signal = plugin.entry_signal(frame, {"lookback": 2})
    assert bool(signal.iloc[-1])
    assert not bool(plugin.exit_signal(frame, {}, {}).iloc[-1])
