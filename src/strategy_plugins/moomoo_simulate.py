"""Explicit Moomoo SIMULATE-only execution boundary."""
from __future__ import annotations


def _is_simulate_account(accounts, acc_id: int) -> bool:
    """Require Moomoo's explicit trading-environment field to be SIMULATE."""
    if accounts is None or "acc_id" not in accounts.columns or "trd_env" not in accounts.columns:
        return False
    rows = accounts[accounts["acc_id"].astype(str) == str(int(acc_id))]
    if rows.empty:
        return False
    return str(rows.iloc[0]["trd_env"]).upper() == "SIMULATE"


class MoomooSimulateExecutor:
    def __init__(self, acc_id: int, host: str = "127.0.0.1", port: int = 11111):
        self.acc_id = int(acc_id)
        self.host = host
        self.port = int(port)
        self._trade = None

    def connect(self) -> None:
        try:
            from moomoo import OpenSecTradeContext, TrdMarket, TrdEnv, RET_OK
        except ImportError as exc:
            raise RuntimeError("install the runtime extra to use Moomoo OpenD") from exc
        self._trd_env = TrdEnv.SIMULATE
        self._ret_ok = RET_OK
        self._trade = OpenSecTradeContext(filter_trdmarket=TrdMarket.US, host=self.host, port=self.port)
        ret, accounts = self._trade.get_acc_list()
        if ret != RET_OK:
            raise RuntimeError(f"could not inspect Moomoo accounts: {accounts}")
        if not _is_simulate_account(accounts, self.acc_id):
            self.close()
            raise RuntimeError("refusing executor: selected account is not confirmed SIMULATE")

    def close(self) -> None:
        if self._trade is not None:
            self._trade.close()
            self._trade = None

    def place_market_order(self, symbol: str, side, quantity: int):
        if self._trade is None:
            raise RuntimeError("connect() must confirm a SIMULATE account first")
        if int(quantity) <= 0:
            raise ValueError("quantity must be positive")
        from moomoo import OrderType, TrdSide
        if side not in (TrdSide.BUY, TrdSide.SELL):
            raise ValueError("side must be Moomoo BUY or SELL")
        ret, data = self._trade.place_order(
            price=0, qty=int(quantity), code=symbol, trd_side=side,
            order_type=OrderType.MARKET, trd_env=self._trd_env, acc_id=self.acc_id,
        )
        if ret != self._ret_ok:
            raise RuntimeError(f"SIMULATE paper order failed: {data}")
        return data
