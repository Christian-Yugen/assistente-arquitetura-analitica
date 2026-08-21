"""Avalia de modo reprodutível o golden dataset agregado da QLT-OUTLIER-012."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.outliers import OutlierProfile
from engine.quality.outliers import OutlierColumnProfile, evaluate_outliers


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/outlier-draft-golden-v1.json"
REPORT_PATH = ROOT / "artifacts/golden/outlier-draft-golden-v1.calibration.json"


def main() -> None:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    true_positive = false_positive = false_negative = 0
    results = []

    for scenario in golden["scenarios"]:
        profile = OutlierColumnProfile(
            name="Coluna Interna",
            outliers=OutlierProfile(**scenario["column"]["outliers"]),
        )
        findings = evaluate_outliers(profile)
        observed = [
            {
                "rule_id": finding["rule_id"],
                "severity": finding["severity"],
                "confidence": finding["confidence"],
                "question": finding["question"] is not None,
            }
            for finding in findings
        ]
        expected = scenario["expected_findings"]
        matched = observed == expected
        if expected and matched:
            true_positive += 1
        elif expected:
            false_negative += 1
        elif observed:
            false_positive += 1
        results.append({"scenario_id": scenario["scenario_id"], "passed": matched})

    report = {
        "calibration_id": "CAL-QLT-OUTLIER-012-001",
        "dataset_id": golden["dataset_id"],
        "rule_id": golden["rule_id"],
        "rule_version": golden["rule_version"],
        "scope": "draft_only",
        "metrics": {"true_positive": true_positive, "false_positive": false_positive, "false_negative": false_negative},
        "production_release": "blocked",
        "scenarios": results,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
