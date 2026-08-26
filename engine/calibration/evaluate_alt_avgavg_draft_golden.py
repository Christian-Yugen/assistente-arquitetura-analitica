"""Calibração determinística do golden estritamente sintético ALT-AVGAVG-008."""
from __future__ import annotations

import json
from pathlib import Path

from engine.alerts.average_of_averages import AverageOfAveragesAlertProfile, classify_average_of_averages_review


def evaluate() -> dict[str, int]:
    root = Path(__file__).resolve().parents[2]
    golden = json.loads((root / "artifacts/golden/alt-avgavg-draft-golden-v1.json").read_text(encoding="utf-8"))
    totals = {"tp": 0, "fp": 0, "fn": 0}
    for case in golden["cases"]:
        profile_data = {**golden["profile_defaults"], **case["overrides"]}
        emitted = classify_average_of_averages_review(AverageOfAveragesAlertProfile(**profile_data)) is not None
        expected = bool(case["expected_finding"])
        if emitted and expected:
            totals["tp"] += 1
        elif emitted and not expected:
            totals["fp"] += 1
        elif not emitted and expected:
            totals["fn"] += 1
    return totals
