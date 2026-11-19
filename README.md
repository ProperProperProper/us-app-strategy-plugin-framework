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

The plugin contracts are not themselves a trading bot. The first real adapter
must connect the contracts to the existing US.APP paper-strategy lab and its
shared database before any plugin can be evaluated or paper-promoted.

Python is the native integration language: run an ARM64 Python build with
native NumPy/Pandas wheels for Moomoo, SQLite, plugins, agents, and supervision.
Use Rust selectively for deterministic CPU-heavy kernels after parity testing;
do not replace working Python orchestration merely for language purity.
