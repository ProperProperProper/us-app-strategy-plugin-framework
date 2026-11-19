# Strategy Plugin Framework

A safety-first plugin framework for quantitative strategy research.

The framework separates replaceable research components from a trusted
evaluation kernel. Plugins may provide strategies, indicators, data adapters,
model proposals, or execution assumptions. The kernel remains authoritative
for chronology, validation, risk, promotion, persistence, and paper execution.

Plugins may not submit orders, bypass promotion, access credentials, execute
arbitrary generated code, or report their own performance evidence.

## Development

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
pytest -q
```

This repository contains no fake market-data fixtures and no toy strategy.
Production integration uses real Moomoo OpenD candles, the deterministic
evaluator, SQLite persistence, and Moomoo `TrdEnv.SIMULATE` paper execution.
Credentials and account identifiers remain local and are never committed.

See [real integration](docs/REAL_INTEGRATION.md) for the actual-data replay
command and the SIMULATE-only order boundary.

The repository includes the first real adapter for the US.APP paper-strategy
lab. It loads real Moomoo candles into SQLite, runs the lab's deterministic
blind replay, and can write a validated `SIMULATE`-only runtime artifact after
the promotion gate passes. It does not enable live trading.

The runtime handoff is validated with a typed Pydantic contract. A malformed
artifact, unsupported interval, non-SIMULATE mode, or malformed plugin
reference cannot be written by the promotion host.

Python is the native integration language: run an ARM64 Python build with
native NumPy/Pandas wheels for Moomoo, SQLite, plugins, agents, and supervision.
Use Rust selectively for deterministic CPU-heavy kernels after parity testing;
do not replace working Python orchestration merely for language purity.
