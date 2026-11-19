import pytest
from pydantic import ValidationError

from strategy_plugins import PaperRuntimeArtifact


def valid_artifact():
    return {
        "plugin": {
            "name": "us-app-donchian-ema",
            "version": "lab-source",
            "python_root": "/tmp/plugin/src",
            "entrypoint": "strategy_plugins.us_app_plugin:USAppStrategyPlugin",
            "constructor": {"lab_root": "/tmp/lab"},
        },
        "params": {"fast": 8, "slow": 21},
        "interval": 10,
        "mode": "SIMULATE",
        "promotion": {
            "baseline": {"total_return_pct": 1.0},
            "candidate": {"total_return_pct": 2.0},
            "replay_protocol": "first_21_complete_sessions_then_one_continuous_unseen_replay",
        },
    }


def test_runtime_artifact_contract_accepts_paper_handoff():
    artifact = PaperRuntimeArtifact.model_validate(valid_artifact())
    assert artifact.mode == "SIMULATE"
    assert artifact.interval == 10


@pytest.mark.parametrize(
    ("field", "value"),
    [("mode", "LIVE"), ("interval", 20), ("promotion", {"bad": True})],
)
def test_runtime_artifact_contract_rejects_unsafe_or_malformed_handoff(field, value):
    payload = valid_artifact()
    payload[field] = value
    with pytest.raises(ValidationError):
        PaperRuntimeArtifact.model_validate(payload)


def test_runtime_artifact_contract_rejects_extra_fields():
    payload = valid_artifact()
    payload["unexpected"] = "model output"
    with pytest.raises(ValidationError):
        PaperRuntimeArtifact.model_validate(payload)
