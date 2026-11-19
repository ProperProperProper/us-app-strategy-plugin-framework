# Real integration

The first adapter uses the existing US.APP lab as the deterministic evaluator
and local Moomoo OpenD as the real candle source.

Install the runtime dependencies:

```sh
python3 -m pip install -e '.[runtime]'
```

Run a real-data replay with OpenD running at `127.0.0.1:11111`:

```sh
python3 scripts/real_us_app_replay.py \
  --lab-root /absolute/path/to/us-app-paper-strategy-lab \
  --db quant_dashboard.sqlite3 \
  --symbol US.APP \
  --start '2026-01-01 09:30:00' \
  --end '2026-11-18 16:00:00' \
  --fetch
```

The command fetches real 10-minute candles, validates and stores them in
SQLite, registers the real US.APP strategy plugin, then calls the existing
evaluator through that plugin boundary. It uses the first 21 complete
sessions for selection and one continuous unseen replay through the latest
candle. It never creates synthetic candles.

`MoomooSimulateExecutor` is the separate paper-order boundary. It confirms the
selected account is `SIMULATE` before placing any order. It has no live-order
mode and receives no credentials from the repository.
