# Plugin architecture

The framework has two layers.

The trusted host owns candle validation, chronological replay, position limits,
promotion, persistence, hot-swap authorization, and paper-only safety. Plugins
are untrusted research extensions until explicitly installed and tested.

Python is the native orchestration layer on Apple Silicon. Moomoo access,
SQLite, plugin loading, provider coordination, and supervision stay in ARM64
Python. Rust is an optional native backend for measured CPU-heavy kernels and
must pass parity tests against the Python reference implementation.

## Plugin categories

- **Strategy:** entry and exit rules plus bounded configuration.
- **Indicator:** causal features calculated from completed candles.
- **Proposal provider:** structured hypotheses from local or hosted models.
- **Data source:** reproducible candle snapshots or broker feeds.
- **Execution model:** fees, slippage, and fill assumptions for research.

Provider and data plugins run behind explicit adapters. The current US.APP
adapter loads the trusted, versioned plugin in the local host process; it does
not claim operating-system sandboxing. A future code-capable plugin must be
isolated before it is enabled. No plugin receives broker credentials or direct
order permissions.

## Promotion boundary

The host evaluates every plugin through the same chronological protocol. For
the originating project that means the first 21 complete sessions are used for
selection, followed by one continuous unseen replay through the latest candle.
A plugin cannot report its own returns or promote itself.

## Versioning

Every plugin declares a name, version, kind, API version, supported intervals,
and capabilities. The registry and promotion artifact record the plugin name,
version, entrypoint, constructor, parameters, and replay evidence. The current
US.APP host does not yet persist the complete manifest fields in every replay
row; the runtime artifact is the authoritative handoff record.

## Real-data boundary

The framework must not use synthetic candles or a demonstration strategy for
research claims. The US.APP integration reads real Moomoo OpenD candles,
validates and persists them in SQLite, evaluates them with the originating
lab's 21-session continuous blind replay, and permits only Moomoo
`TrdEnv.SIMULATE` paper execution. Live trading is outside the project scope.
