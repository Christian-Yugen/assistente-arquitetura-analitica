import json
import unittest

from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.contracts.validation import validate_diagnosis_root
from engine.pipeline.quality_diagnosis import DiagnosisMetadata, build_column_analysis_context, execute_quality_diagnosis


METADATA = DiagnosisMetadata(
    analysis_id="00000000-0000-4000-8000-000000000101",
    project_id="00000000-0000-4000-8000-000000000102",
    owner_user_id="00000000-0000-4000-8000-000000000103",
    project_name="Projeto de teste",
    objective="Validar diagnóstico reconstruído de nulos.",
    file_id="00000000-0000-4000-8000-000000000104",
    original_name="entrada.xlsx",
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


class NullPipelineTests(unittest.TestCase):
    def test_aggregates_missingness_and_adapts_high_ratio_to_the_canonical_contract(self):
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000110",
            column_id="00000000-0000-4000-8000-000000000111",
            column_name="Observação",
            values=["texto seguro"] * 16 + [None] * 4,
            sheet_name="Aba segura",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )
        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertEqual(context.missingness.observed_cell_count, 20)
        self.assertEqual(context.missingness.structural_null_count, 4)
        self.assertEqual(context.missingness.missing_ratio, 0.2)
        self.assertEqual(diagnosis["summary"]["counts"]["risks"], 1)
        self.assertEqual(diagnosis["findings"][0]["rule_id"], "QLT-NULL-001")
        self.assertEqual(diagnosis["findings"][0]["rule_version"], "0.1.0-reconstructed.1")
        self.assertEqual(diagnosis["questions"][0]["impact"]["affected_rule_ids"], ["QLT-NULL-001"])
        self.assertEqual(diagnosis["summary"]["completeness_ratio"], round(2 / METADATA.execution_profile.catalog_target_rule_count, 8))
        self.assertNotIn("texto seguro", serialized)
        validate_diagnosis_root(diagnosis)


if __name__ == "__main__":
    unittest.main()
