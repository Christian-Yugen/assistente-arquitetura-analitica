import hashlib
import json
import unittest
from pathlib import Path

from engine.alerts.entity_association import EntityAssociationProfile, classify_entity_association
from engine.calibration.evaluate_grn_assoc_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS, to_diagnosis_fragment
from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.pipeline.quality_diagnosis import DiagnosisMetadata, build_column_analysis_context, execute_quality_diagnosis


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts" / "golden"
METADATA = DiagnosisMetadata(
    analysis_id="00000000-0000-4000-8000-000000000301",
    project_id="00000000-0000-4000-8000-000000000302",
    owner_user_id="00000000-0000-4000-8000-000000000303",
    project_name="Projeto sintético",
    objective="Verificar supressão controlada de associação entre entidades.",
    file_id="00000000-0000-4000-8000-000000000304",
    original_name="entrada-sintetica.xlsx",
    file_size_bytes=1024,
    file_sha256="d" * 64,
    file_mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    workbook_readable=True,
    consented_at="2026-08-26T00:00:00Z",
    created_at="2026-08-26T00:00:00Z",
    uploaded_at="2026-08-26T00:00:00Z",
    retention_delete_at="2026-08-27T00:00:00Z",
    retention_status="scheduled",
    correlation_id="00000000-0000-4000-8000-000000000305",
    terms_version="1.0",
    domain="generic",
    business_questions=(),
    analysis_version=1,
    supersedes_analysis_id=None,
    execution_profile=load_authorized_draft_profile(),
)


class EntityAssociationTests(unittest.TestCase):
    def test_emits_only_for_independent_aggregate_signal(self):
        finding = classify_entity_association(EntityAssociationProfile(independent_association_signal_count=1))

        self.assertEqual(finding["rule_id"], "GRN-ASSOC-007")
        self.assertEqual(finding["category"], "grain")
        self.assertTrue(finding["question"]["blocking"])

    def test_blocks_missing_signal_confirmation_conflict_sensitivity_and_contract_error(self):
        for profile in (
            EntityAssociationProfile(),
            EntityAssociationProfile(independent_association_signal_count=1, confirmed_association_count=1),
            EntityAssociationProfile(independent_association_signal_count=1, structural_conflict_count=1),
            EntityAssociationProfile(independent_association_signal_count=1, sensitive_signal_count=1),
            EntityAssociationProfile(independent_association_signal_count=1, contract_error_count=1),
        ):
            self.assertIsNone(classify_entity_association(profile))

    def test_projects_only_aggregate_finding_with_registered_version(self):
        finding = classify_entity_association(EntityAssociationProfile(independent_association_signal_count=2))
        fragment = to_diagnosis_fragment([finding], sheet_id="opaque-sheet", column_id=None)

        self.assertEqual(RULE_VERSIONS["GRN-ASSOC-007"], "0.1.0-provisional.1")
        self.assertEqual(fragment["findings"][0]["rule_id"], "GRN-ASSOC-007")
        self.assertEqual(fragment["findings"][0]["rule_version"], "0.1.0-provisional.1")
        self.assertEqual(fragment["findings"][0]["evidence"][0]["observed"], {"observed_value": 2})

    def test_synthetic_golden_hash_calibration_and_fail_closed_cases(self):
        manifest = json.loads((GOLDEN_DIR / "grn-assoc-draft-golden-v1.manifest.json").read_text(encoding="utf-8"))
        golden_path = GOLDEN_DIR / manifest["file"]
        golden = json.loads(golden_path.read_text(encoding="utf-8"))

        self.assertTrue(manifest["synthetic_only"])
        self.assertFalse(manifest["production_authorized"])
        self.assertEqual(manifest["calibration"], {"tp": 1, "fp": 0, "fn": 0})
        self.assertEqual(hashlib.sha256(golden_path.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), manifest["calibration"])

        for case in golden["cases"]:
            profile = EntityAssociationProfile(**(golden["profile_defaults"] | case["overrides"]))
            self.assertEqual(classify_entity_association(profile) is not None, case["expected_finding"])

    def test_real_pipeline_fixes_signal_at_zero_and_does_not_emit_entity_association(self):
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000310",
            column_id="00000000-0000-4000-8000-000000000311",
            column_name="Campo sintético",
            values=["valor sintético"],
            sheet_name="Aba sintética",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )
        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)

        self.assertNotIn("GRN-ASSOC-007", {finding["rule_id"] for finding in diagnosis["findings"]})


if __name__ == "__main__":
    unittest.main()

