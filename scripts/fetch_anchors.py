#!/usr/bin/env python3
"""Fetch World Bank anchors and save data/anchors.json (run from repo root)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from poc_abm.data_worldbank import build_anchors  # noqa: E402

anchors = build_anchors()
print(json.dumps(anchors, indent=2))
out = Path(__file__).resolve().parent / "data" / "anchors.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(anchors, indent=2))
print("\nsaved to data/anchors.json")
