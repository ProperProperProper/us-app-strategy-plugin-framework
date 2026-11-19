from strategy_plugins import PluginManifest, PluginRegistry
from strategy_plugins.moomoo_simulate import _is_simulate_account
import pandas as pd


class Dummy:
    manifest = PluginManifest("dummy", "1.0.0", "strategy")


def test_explicit_registration_and_lookup():
    registry = PluginRegistry()
    manifest = registry.register(Dummy())
    assert registry.get("strategy", "dummy").manifest == manifest


def test_duplicate_registration_is_rejected():
    registry = PluginRegistry()
    registry.register(Dummy())
    try:
        registry.register(Dummy())
    except ValueError as exc:
        assert "already registered" in str(exc)
    else:
        raise AssertionError("duplicate plugin registration was accepted")


def test_simulate_executor_requires_explicit_environment_column():
    accounts = pd.DataFrame([
        {"acc_id": 12, "trd_env": "SIMULATE", "competition_acc_name": "paper"},
        {"acc_id": 13, "trd_env": "REAL", "competition_acc_name": "SIMULATE description"},
    ])
    assert _is_simulate_account(accounts, 12)
    assert not _is_simulate_account(accounts, 13)
    assert not _is_simulate_account(accounts.drop(columns=["trd_env"]), 12)
