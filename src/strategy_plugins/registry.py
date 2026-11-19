"""Explicit registry for locally installed plugins."""
from __future__ import annotations

from typing import Any
from .contracts import PluginManifest, PluginRecord


class PluginRegistry:
    """Discovery never executes model-generated code; registration is explicit."""
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], PluginRecord] = {}

    def register(self, plugin: Any) -> PluginManifest:
        manifest = getattr(plugin, "manifest", None)
        if not isinstance(manifest, PluginManifest):
            raise TypeError("plugin must expose a PluginManifest named manifest")
        if not manifest.name or not manifest.version or not manifest.kind:
            raise ValueError("plugin manifest requires name, version, and kind")
        key = (manifest.kind, manifest.name)
        if key in self._records:
            raise ValueError(f"plugin already registered: {manifest.kind}/{manifest.name}")
        self._records[key] = PluginRecord(manifest, plugin)
        return manifest

    def get(self, kind: str, name: str) -> Any:
        try:
            return self._records[(kind, name)].plugin
        except KeyError as exc:
            raise KeyError(f"unknown plugin: {kind}/{name}") from exc

    def manifests(self) -> tuple[PluginManifest, ...]:
        return tuple(record.manifest for record in self._records.values())
