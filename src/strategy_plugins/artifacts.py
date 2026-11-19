"""Typed, provider-independent contract for the paper-runtime handoff."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class PluginReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    python_root: str = Field(min_length=1)
    entrypoint: str = Field(pattern=r"^[A-Za-z_][\w.]*:[A-Za-z_][\w]*$")
    constructor: dict[str, Any] = Field(default_factory=dict)


class PromotionEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    baseline: dict[str, Any]
    candidate: dict[str, Any]
    replay_protocol: Literal[
        "first_21_complete_sessions_then_one_continuous_unseen_replay"
    ]


class PaperRuntimeArtifact(BaseModel):
    """Only artifact shape accepted by the structural paper-bot loader."""

    model_config = ConfigDict(extra="forbid")

    plugin: PluginReference
    params: dict[str, Any]
    interval: Literal[10]
    mode: Literal["SIMULATE"]
    promotion: PromotionEvidence

