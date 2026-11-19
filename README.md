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

This repository is research-only. It contains no broker credentials, account
identifiers, live-order adapter, or production trading code.
