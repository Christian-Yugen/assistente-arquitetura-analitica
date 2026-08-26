from __future__ import annotations

import json
from pathlib import Path

from engine.alerts.pre_aggregation import PreAggregationProfile, classify_pre_aggregation


def evaluate() -> dict[str, int]:
    root = Path(__file__).resolve().parents[2]
    golden = json.loads((root / "artifacts/golden/grn-preagg-draft-golden-v1.json").read_text(encoding="utf-8"))
    totals = {"tp": 0, "fp": 0, "fn": 0}
    for case in golden["cases"]:
        emitted = classify_pre_aggregation(PreAggregationProfile(**{**golden["profile_defaults"], **case["overrides"]})) is not None
        expected = bool(case["expected_finding"])
        if emitted and expected:
            totals["tp"] += 1
        elif emitted and not expected:
            totals["fp"] += 1
        elif not emitted and expected:
            totals["fn"] += 1
    return totals

