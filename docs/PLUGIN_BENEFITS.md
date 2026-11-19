# Why the strategy runs as a plugin

The strategy is a plugin so strategy research can evolve without destabilizing
the paper bot, broker adapter, dashboard, or persistence layer.

## Operational benefits

- **Hot swapping:** an approved strategy implementation can be loaded at a
  completed-candle boundary without restarting the paper bot.
- **Safe rollback:** malformed or incompatible plugin artifacts are rejected;
  the bot keeps the last known-good strategy.
- **Promotion control:** plugins cannot promote themselves. The trusted host
  evaluates the candidate and writes the runtime handoff only after the replay
  gate passes.
- **Paper-only boundary:** the current runtime artifact is restricted to
  Moomoo `SIMULATE` execution. Plugins receive no credentials or direct order
  API.
- **Consistent comparisons:** every registered strategy uses the same candle
  validation, chronology, 21-session selection boundary, continuous unseen
  replay, risk checks, and evidence format.

## Research and maintenance benefits

- **Separation of concerns:** strategy rules, indicators, data sources,
  execution assumptions, providers, supervision, and storage have explicit
  interfaces.
- **Variant research:** parameter changes and structural strategy variants can
  be tested without editing the bot's execution kernel.
- **Provider independence:** local MLX, NVIDIA, Apple private-cloud, and
  Antigravity may propose or review hypotheses, but none can calculate
  authoritative performance or bypass promotion.
- **Versioned evidence:** the plugin identity, parameters, replay evidence, and
  runtime handoff remain attributable after a strategy changes.
- **Portability:** another machine can install the framework, point it at the
  same lab and data snapshot, and reproduce the evaluation boundary.
- **Extensibility:** future indicators, data adapters, execution models, and
  proposal providers can be added behind contracts rather than copied into the
  core bot.

## Current boundary

The real US.APP plugin is trusted local Python integration code and currently
loads in the paper-bot process; it is not an operating-system sandbox. The
plugin framework validates the runtime artifact, but the deterministic local
evaluator remains the authority for fills, returns, drawdown, trade counts, and
promotion.
