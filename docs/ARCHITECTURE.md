# Plugin architecture

The framework has two layers.

The trusted host owns candle validation, chronological replay, position limits,
promotion, persistence, hot-swap authorization, and paper-only safety. Plugins
are untrusted research extensions until explicitly installed and tested.

## Plugin categories

- **Strategy:** entry and exit rules plus bounded configuration.
- **Indicator:** causal features calculated from completed candles.
- **Proposal provider:** structured hypotheses from local or hosted models.
- **Data source:** reproducible candle snapshots or broker feeds.
- **Execution model:** fees, slippage, and fill assumptions for research.

Provider and data plugins should eventually run in isolated subprocesses. A
plugin must never receive broker credentials or direct order permissions.

## Promotion boundary

The host evaluates every plugin through the same chronological protocol. For
the originating project that means the first 21 complete sessions are used for
selection, followed by one continuous unseen replay through the latest candle.
A plugin cannot report its own returns or promote itself.

## Versioning

Every plugin declares a name, version, kind, API version, supported intervals,
and capabilities. The host records the manifest beside every evaluation so
results remain attributable after a plugin changes.
