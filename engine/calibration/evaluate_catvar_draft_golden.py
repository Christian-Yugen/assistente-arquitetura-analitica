"""Avalia a fixture golden agregada da QLT-CATVAR-008 antes de sua ativação draft."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.categorical_variations import CategoricalVariationProfile
from engine.quality.catvar import CategoricalVariationColumnProfile, evaluate_categorical_variations


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/catvar-draft-golden-v1.json"
REPORT_PATH = ROOT / "artifacts/golden/catvar-draft-golden-v1.calibration.json"


def _signature(item: dict[str, object]) -> tuple[str, str, float, bool]:
    return (str(item["rule_id"]), str(item["severity"]), float(item["confidence"]), bool(item["question"]))


def evaluate() -> dict[str, object]:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    totals = {"true_positive": 0, "false_positive": 0, "false_negative": 0}
    scenarios: list[dict[str, object]] = []
    for scenario in golden["scenarios"]:
        column = scenario["column"]
        findings = evaluate_categorical_variations(
            CategoricalVariationColumnProfile(
                name="golden_column",
                physical_type=column["physical_type"],
                variations=CategoricalVariationProfile(**column["variations"]),
            )
        )
        expected = {_signature(item) for item in scenario["expected_findings"]}
        actual = {_signature(item) for item in findings}
        totals["true_positive"] += len(actual & expected)
        totals["false_positive"] += len(actual - expected)
        totals["false_negative"] += len(expected - actual)
        scenarios.append(
            {
                "case_id": scenario["case_id"],
                "expected_signatures": [list(signature) for signature in sorted(expected)],
                "actual_signatures": [list(signature) for signature in sorted(actual)],
                "status": "pass" if actual == expected else "mismatch",
            }
        )
    return {
        "report_id": "CAL-QLT-CATVAR-008-001",
        "dataset_id": golden["dataset_id"],
        "dataset_version": golden["version"],
        "rules": {"QLT-CATVAR-008": totals},
        "scenario_count": len(scenarios),
        "mismatch_count": sum(item["status"] != "pass" for item in scenarios),
        "scenarios": scenarios,
        "decision": "calibrated_for_provisional_draft" if all(item["status"] == "pass" for item in scenarios) else "requires_review",
        "production_status": "blocked",
        "catalog_activation_status": "pending_calibration_gate",
    }


def main() -> None:
    report = evaluate()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
