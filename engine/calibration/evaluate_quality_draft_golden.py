"""Avalia a fixture golden das regras de qualidade autorizadas no perfil draft."""

from __future__ import annotations

import json
from pathlib import Path

from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.pipeline.quality_diagnosis import ColumnAnalysisContext, DiagnosisMetadata, execute_quality_diagnosis
from engine.profiling.missingness import MissingnessProfile
from engine.profiling.numeric_text import NumericTextProfile


ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "artifacts/golden/quality-draft-golden-v1.json"
REPORT_PATH = ROOT / "artifacts/golden/quality-draft-golden-v1.calibration.json"


def _metadata() -> DiagnosisMetadata:
    return DiagnosisMetadata(
        analysis_id="00000000-0000-4000-8000-000000000201",
        project_id="00000000-0000-4000-8000-000000000202",
        owner_user_id="00000000-0000-4000-8000-000000000203",
        project_name="Golden calibration",
        objective="Calibrar regras draft com perfis agregados.",
        file_id="00000000-0000-4000-8000-000000000204",
        original_name="golden.xlsx",
        file_size_bytes=1024,
        file_sha256="c" * 64,
        file_mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        workbook_readable=True,
        consented_at="2026-08-20T00:00:00Z",
        created_at="2026-08-20T00:00:00Z",
        uploaded_at="2026-08-20T00:00:00Z",
        retention_delete_at="2026-08-21T00:00:00Z",
        retention_status="scheduled",
        correlation_id="00000000-0000-4000-8000-000000000205",
        terms_version="1.0",
        domain="generic",
        business_questions=(),
        analysis_version=1,
        supersedes_analysis_id=None,
        execution_profile=load_authorized_draft_profile(),
    )


def _signature(item: dict[str, object]) -> tuple[str, str, bool]:
    return (str(item["rule_id"]), str(item["severity"]), bool(item["question"]))


def evaluate() -> dict[str, object]:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    by_rule: dict[str, dict[str, int]] = {
        "QLT-NUMTEXT-007": {"true_positive": 0, "false_positive": 0, "false_negative": 0},
        "QLT-NULL-001": {"true_positive": 0, "false_positive": 0, "false_negative": 0},
    }
    tracked_rule_ids = frozenset(by_rule)
    scenarios: list[dict[str, object]] = []

    for position, scenario in enumerate(golden["scenarios"]):
        column = scenario["column"]
        context = ColumnAnalysisContext(
            sheet_id=f"00000000-0000-4000-8000-{3000 + position:012d}",
            sheet_name=f"golden-sheet-{position}",
            sheet_position=position,
            sheet_visibility="visible",
            column_id=f"00000000-0000-4000-8000-{4000 + position:012d}",
            column_name="golden_column",
            column_position=0,
            physical_type=column["physical_type"],
            numeric_text=NumericTextProfile(**column["numeric_text"]),
            missingness=MissingnessProfile(**column["missingness"]),
        )
        diagnosis = execute_quality_diagnosis([context], metadata=_metadata())
        expected = {_signature(item) for item in scenario["expected_findings"]}
        actual = {
            (
                str(finding["rule_id"]),
                str(finding["severity"]),
                any(finding["rule_id"] in question["impact"]["affected_rule_ids"] for question in diagnosis["questions"]),
            )
            for finding in diagnosis["findings"]
            if str(finding["rule_id"]) in tracked_rule_ids
        }
        for rule_id, severity, question in actual & expected:
            by_rule[rule_id]["true_positive"] += 1
        for rule_id, severity, question in actual - expected:
            by_rule[rule_id]["false_positive"] += 1
        for rule_id, severity, question in expected - actual:
            by_rule[rule_id]["false_negative"] += 1
        scenarios.append(
            {
                "case_id": scenario["case_id"],
                "expected_signatures": [list(signature) for signature in sorted(expected)],
                "actual_signatures": [list(signature) for signature in sorted(actual)],
                "status": "pass" if actual == expected else "mismatch",
            }
        )

    return {
        "report_id": "CAL-QUALITY-DRAFT-001",
        "dataset_id": golden["dataset_id"],
        "dataset_version": golden["version"],
        "rules": by_rule,
        "scenario_count": len(scenarios),
        "mismatch_count": sum(item["status"] != "pass" for item in scenarios),
        "scenarios": scenarios,
        "decision": "calibrated_for_draft" if all(item["status"] == "pass" for item in scenarios) else "requires_review",
        "production_status": "blocked",
    }


def main() -> None:
    report = evaluate()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
