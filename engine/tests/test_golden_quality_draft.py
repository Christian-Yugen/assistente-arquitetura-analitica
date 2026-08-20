import json
import unittest
from hashlib import sha256
from pathlib import Path

from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.contracts.validation import validate_diagnosis_root
from engine.pipeline.quality_diagnosis import (
    ColumnAnalysisContext,
    DiagnosisMetadata,
    execute_quality_diagnosis,
)
from engine.profiling.missingness import MissingnessProfile
from engine.profiling.numeric_text import NumericTextProfile
from engine.quality.nulls import NullColumnProfile, evaluate_nulls
from engine.quality.numtext import NumericTextColumnProfile, evaluate_numeric_text


GOLDEN_PATH = Path(__file__).resolve().parents[2] / "artifacts/golden/quality-draft-golden-v1.json"
MANIFEST_PATH = Path(__file__).resolve().parents[2] / "artifacts/golden/quality-draft-golden-v1.manifest.json"


METADATA = DiagnosisMetadata(
    analysis_id="00000000-0000-4000-8000-000000000101",
    project_id="00000000-0000-4000-8000-000000000102",
    owner_user_id="00000000-0000-4000-8000-000000000103",
    project_name="Golden calibration",
    objective="Calibrar regras draft com perfis agregados.",
    file_id="00000000-0000-4000-8000-000000000104",
    original_name="golden.xlsx",
    file_size_bytes=1024,
    file_sha256="b" * 64,
    file_mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    workbook_readable=True,
    consented_at="2026-08-20T00:00:00Z",
    created_at="2026-08-20T00:00:00Z",
    uploaded_at="2026-08-20T00:00:00Z",
    retention_delete_at="2026-08-21T00:00:00Z",
    retention_status="scheduled",
    correlation_id="00000000-0000-4000-8000-000000000105",
    terms_version="1.0",
    domain="generic",
    business_questions=(),
    analysis_version=1,
    supersedes_analysis_id=None,
    execution_profile=load_authorized_draft_profile(),
)


class GoldenQualityDraftTests(unittest.TestCase):
    def test_all_aggregate_golden_cases_match_findings_questions_and_privacy_expectations(self):
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(golden["dataset_id"], "GD-QUALITY-DRAFT-001")
        self.assertEqual(manifest["dataset_id"], golden["dataset_id"])
        self.assertEqual(manifest["status"], "approved_for_draft_calibration")
        self.assertEqual(manifest["sha256"], sha256(GOLDEN_PATH.read_bytes()).hexdigest())
        self.assertTrue(golden["privacy"]["contains_raw_workbook_values"] is False)
        self.assertTrue(golden["privacy"]["contains_original_sheet_titles"] is False)
        self.assertTrue(golden["privacy"]["contains_personal_data"] is False)

        for position, scenario in enumerate(golden["scenarios"]):
            column = scenario["column"]
            context = ColumnAnalysisContext(
                sheet_id=f"00000000-0000-4000-8000-{1000 + position:012d}",
                sheet_name=f"golden-sheet-{position}",
                sheet_position=position,
                sheet_visibility="visible",
                column_id=f"00000000-0000-4000-8000-{2000 + position:012d}",
                column_name="golden_column",
                column_position=0,
                physical_type=column["physical_type"],
                numeric_text=NumericTextProfile(**column["numeric_text"]),
                missingness=MissingnessProfile(**column["missingness"]),
            )
            internal_findings = [
                *evaluate_numeric_text(
                    NumericTextColumnProfile(
                        name=context.column_name,
                        physical_type=context.physical_type,  # type: ignore[arg-type]
                        **column["numeric_text"],
                    )
                ),
                *evaluate_nulls(
                    NullColumnProfile(
                        name=context.column_name,
                        physical_type=context.physical_type,
                        missingness=context.missingness,
                    )
                ),
            ]
            internal_observed = [
                {
                    "rule_id": finding["rule_id"],
                    "severity": finding["severity"],
                    "confidence": finding["confidence"],
                    "question": finding["question"] is not None,
                }
                for finding in internal_findings
            ]
            self.assertCountEqual(internal_observed, scenario["expected_findings"], msg=scenario["case_id"])

            diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
            validate_diagnosis_root(diagnosis)

            observed = [
                {
                    "rule_id": finding["rule_id"],
                    "severity": finding["severity"],
                    "question": any(
                        finding["rule_id"] in question["impact"]["affected_rule_ids"]
                        for question in diagnosis["questions"]
                    ),
                }
                for finding in diagnosis["findings"]
            ]
            canonical_expected = [
                {
                    "rule_id": expectation["rule_id"],
                    "severity": expectation["severity"],
                    "question": expectation["question"],
                }
                for expectation in scenario["expected_findings"]
            ]
            self.assertCountEqual(observed, canonical_expected, msg=scenario["case_id"])

            serialized = json.dumps(diagnosis)
            self.assertNotIn("raw_values", serialized)
            self.assertNotIn("original_sheet_title", serialized)
            self.assertNotIn("sensitive_example", serialized)
