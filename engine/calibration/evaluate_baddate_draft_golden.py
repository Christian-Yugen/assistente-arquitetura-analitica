"""Avalia a calibração isolada e reprodutível da QLT-BADDATE-006 no perfil draft."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.bad_dates import BadDateProfile
from engine.quality.bad_dates import BadDateColumnProfile, evaluate_bad_dates


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/baddate-draft-golden-v1.json"
REPORT_PATH = ROOT / "artifacts/golden/baddate-draft-golden-v1.calibration.json"


def signature(finding: dict[str, object]) -> dict[str, object]:
    return {
        "rule_id": finding["rule_id"],
        "severity": finding["severity"],
        "confidence": finding["confidence"],
        "question": finding["question"] is not None,
    }


def evaluate() -> dict[str, object]:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    scenarios: list[dict[str, object]] = []
    true_positive = false_positive = false_negative = 0
    for scenario in golden["scenarios"]:
        profile = BadDateColumnProfile(name="Coluna 1", bad_dates=BadDateProfile(**scenario["column"]["bad_dates"]))
        actual = [signature(finding) for finding in evaluate_bad_dates(profile)]
        expected = scenario["expected_findings"]
        actual_serialized = {json.dumps(item, sort_keys=True) for item in actual}
        expected_serialized = {json.dumps(item, sort_keys=True) for item in expected}
        true_positive += len(actual_serialized & expected_serialized)
        false_positive += len(actual_serialized - expected_serialized)
        false_negative += len(expected_serialized - actual_serialized)
        scenarios.append({"case_id": scenario["case_id"], "status": "pass" if actual_serialized == expected_serialized else "mismatch", "expected_count": len(expected), "actual_count": len(actual)})

    report = {
        "calibration_id": "CAL-QLT-BADDATE-006-001",
        "dataset_id": golden["dataset_id"],
        "rule_id": "QLT-BADDATE-006",
        "rule_version": "0.1.0-provisional.1",
        "scope": "draft_only",
        "production_release": "blocked",
        "metrics": {"true_positive": true_positive, "false_positive": false_positive, "false_negative": false_negative},
        "scenarios": scenarios,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
