"""Avalia a calibração agregada e reprodutível da QLT-IDMISS-015."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.identifier_completeness import IdentifierCompletenessProfile
from engine.quality.identifier_completeness import IdentifierCompletenessColumnProfile, evaluate_identifier_completeness


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = PROJECT_ROOT / "artifacts/golden/idmiss-draft-golden-v1.json"
REPORT_PATH = PROJECT_ROOT / "artifacts/golden/idmiss-draft-golden-v1.calibration.json"


def _reduced(findings: list[dict[str, object]]) -> list[dict[str, object]]:
    return [{"rule_id": finding["rule_id"], "severity": finding["severity"], "question": finding["question"] is not None} for finding in findings]


def evaluate() -> dict[str, object]:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    true_positive = false_positive = false_negative = 0
    results = []
    for scenario in golden["scenarios"]:
        profile = IdentifierCompletenessProfile(**scenario["profile"])
        observed = _reduced(evaluate_identifier_completeness(IdentifierCompletenessColumnProfile("Field", profile)))
        expected = scenario["expected_findings"]
        if observed == expected and expected:
            true_positive += 1
        elif observed and not expected:
            false_positive += 1
        elif not observed and expected:
            false_negative += 1
        results.append({"scenario_id": scenario["scenario_id"], "passed": observed == expected})
    report = {
        "calibration_id": "CAL-QLT-IDMISS-015-001",
        "dataset_id": golden["dataset_id"],
        "rule_id": golden["rule_id"],
        "scope": "draft_only",
        "metrics": {"true_positive": true_positive, "false_positive": false_positive, "false_negative": false_negative},
        "production_release": "blocked",
        "scenarios": results,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
