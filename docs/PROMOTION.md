# Plugin promotion

The host, not a plugin or model, decides promotion.

For each candidate the host freshly evaluates the unchanged baseline and the
candidate using the first 21 complete sessions for selection, followed by one
continuous unseen replay through the latest candle. The default gate requires:

- replay status `OK`;
- at least three replay trades;
- candidate replay return above the fresh baseline; and
- no more than one percentage point of additional drawdown.

Passing evidence creates a local `SIMULATE` runtime artifact containing the
plugin identity, version, parameters, and replay evidence. The artifact is
written atomically. It does not submit an order and it is not a live-trading
credential or authorization.
