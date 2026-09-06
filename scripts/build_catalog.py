#!/usr/bin/env python3
"""Build the public catalog from individual plugin manifests."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins"
CATALOG = ROOT / "catalog.json"

plugins = []
for path in sorted(PLUGIN_DIR.glob("*.json")):
    with path.open(encoding="utf-8") as handle:
        plugins.append(json.load(handle))

plugins.sort(key=lambda plugin: plugin["id"])
with CATALOG.open("w", encoding="utf-8") as handle:
    json.dump(plugins, handle, ensure_ascii=False, indent=2)
    handle.write("\n")
