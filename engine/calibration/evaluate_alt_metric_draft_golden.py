"""Calibração determinística do golden estritamente sintético ALT-METRIC-006."""
from __future__ import annotations

import json
from pathlib import Path

from engine.alerts.metric_risk import PotentiallyMisleadingMetricAlertProfile, classify_potentially_misleading_metric_review


def evaluate() -> dict[str, int]:
    root = Path(__file__).resolve().parents[2]
    golden = json.loads((root / "artifacts/golden/alt-metric-draft-golden-v1.json").read_text(encoding="utf-8"))
    totals = {"tp": 0, "fp": 0, "fn": 0}
    for case in golden["cases"]:
        profile_data = {**golden["profile_defaults"], **case["overrides"]}
        emitted = classify_potentially_misleading_metric_review(PotentiallyMisleadingMetricAlertProfile(**profile_data)) is not None
        expected = bool(case["expected_finding"])
        if emitted and expected:
            totals["tp"] += 1
        elif emitted and not expected:
            totals["fp"] += 1
        elif not emitted and expected:
            totals["fn"] += 1
    return totals
