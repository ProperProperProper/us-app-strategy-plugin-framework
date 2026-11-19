from strategy_plugins import PluginManifest, PluginRegistry


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
