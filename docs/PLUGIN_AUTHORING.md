# Plugin authoring

Start with a manifest and implement only the contract for the plugin kind.
Keep configuration serializable and bounded. Reject invalid configuration
before calculating features or signals.

Do not add toy strategies or synthetic market data to demonstrate a plugin.
Use a real captured data snapshot or the live Moomoo OpenD adapter in an
explicit paper-test run, and record the source, timestamp range, commit, and
execution model.

Indicators and strategies must be causal: the value at candle `t` may use only
completed candles at or before `t`. Do not use future candles, hidden labels,
broker state, credentials, or order-submission APIs.

Add deterministic tests for warm-up behavior, duplicate inputs, unsupported
intervals, and signal output. Register the plugin explicitly; the registry
does not discover or execute model-generated modules. The trusted host—not the
plugin—owns metrics, walk-forward replay, promotion, and persistence.
