import copy
import json
import unittest
from dataclasses import replace

from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.contracts.validation import validate_diagnosis_root
from engine.catalog import executable_rule_count
from engine.pipeline.quality_diagnosis import DiagnosisMetadata, build_column_analysis_context, execute_quality_diagnosis


METADATA = DiagnosisMetadata(
    analysis_id="00000000-0000-4000-8000-000000000001",
    project_id="00000000-0000-4000-8000-000000000002",
    owner_user_id="00000000-0000-4000-8000-000000000003",
    project_name="Projeto de teste",
    objective="Validar diagnóstico parcial de qualidade.",
    file_id="00000000-0000-4000-8000-000000000004",
    original_name="entrada.xlsx",
    file_size_bytes=1024,
    file_sha256="a" * 64,
    file_mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    workbook_readable=True,
    consented_at="2026-08-20T00:00:00Z",
    created_at="2026-08-20T00:00:00Z",
    uploaded_at="2026-08-20T00:00:00Z",
    retention_delete_at="2026-08-21T00:00:00Z",
    retention_status="scheduled",
    correlation_id="00000000-0000-4000-8000-000000000005",
    terms_version="1.0",
    domain="generic",
    business_questions=(),
    analysis_version=1,
    supersedes_analysis_id=None,
    execution_profile=load_authorized_draft_profile(),
)


class NumericTextPipelineTests(unittest.TestCase):
    def test_profiles_aggregate_numeric_text_fields_and_discards_raw_values_from_context(self):
        context = build_column_analysis_context(
            sheet_id="sheet-sales",
            column_id="column-total",
            column_name="Total",
            values=["1200", "2.5", "codigo-A", "1,234", "", None],
            sheet_name="Vendas",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        self.assertEqual(context.physical_type, "text")
        self.assertEqual(context.numeric_text.non_empty_value_count, 4)
        self.assertEqual(context.numeric_text.numeric_text_candidate_count, 2)
        self.assertEqual(context.numeric_text.numeric_text_candidate_ratio, 0.5)
        self.assertEqual(context.numeric_text.numeric_text_basis, "strict_canonical_numeric_string")
        self.assertEqual(context.numeric_text.numeric_text_ambiguity_count, 1)
        self.assertFalse(hasattr(context.numeric_text, "raw_values"))

    def test_executes_context_to_rule_to_canonical_diagnosis_root(self):
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Total",
            values=["1200", "2.5", "codigo-A", "1,234"],
            sheet_name="Vendas",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis(
            [context], metadata=METADATA
        )
        serialized = json.dumps(diagnosis)

        self.assertEqual(diagnosis["schema_version"], "1.0.0")
        self.assertEqual(diagnosis["contract_id"], "PM-MVP-PBI-CON-001")
        self.assertEqual(diagnosis["summary"]["counts"]["risks"], 1)
        self.assertEqual(len(diagnosis["questions"]), 1)
        self.assertEqual(diagnosis["findings"][0]["rule_id"], "QLT-NUMTEXT-007")
        self.assertEqual(diagnosis["questions"][0]["impact"]["affected_rule_ids"], ["QLT-NUMTEXT-007"])
        validate_diagnosis_root(diagnosis)
        self.assertNotIn("1200", serialized)
        self.assertNotIn("codigo-A", serialized)

    def test_projects_sensitivity_in_its_segregated_collection_without_exposing_input_content(self):
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="CPF",
            values=["__PIPELINE_SYNTHETIC_OBSERVATION__"],
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertEqual(len(diagnosis["sensitivity_classifications"]), 1)
        self.assertEqual(diagnosis["sensitivity_classifications"][0]["sensitivity"], "personal_data_candidate")
        self.assertNotIn("personal_data_candidate", [item.get("semantic_type") for item in diagnosis["semantic_classifications"]])
        self.assertTrue(diagnosis["questions"][0]["blocking"])
        self.assertNotIn("CPF", serialized)
        self.assertNotIn("__PIPELINE_SYNTHETIC_OBSERVATION__", serialized)

    def test_projects_competence_as_semantic_type_without_exposing_header_or_dates(self):
        values = [f"2026-07-{day:02d}" for day in range(1, 11)]
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Data de competência",
            values=values,
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertIn("competence_date_candidate", [item["semantic_type"] for item in diagnosis["semantic_classifications"]])
        self.assertNotIn("Data de competência", serialized)
        self.assertNotIn("2026-07-01", serialized)

    def test_projects_description_as_semantic_type_without_exposing_header_or_text_content(self):
        values = [f"rotulo-sintetico-{index:02d}" for index in range(1, 11)]
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Descrição",
            values=values,
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertIn("name_or_description_candidate", [item["semantic_type"] for item in diagnosis["semantic_classifications"]])
        self.assertNotIn("Descrição", serialized)
        self.assertNotIn("rotulo-sintetico-01", serialized)

    def test_projects_duration_as_semantic_type_without_exposing_header_or_numeric_content(self):
        values = list(range(101001, 101011))
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Duração (horas)",
            values=values,
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertIn("duration_candidate", [item["semantic_type"] for item in diagnosis["semantic_classifications"]])
        self.assertNotIn("Duração (horas)", serialized)
        self.assertNotIn("101001", serialized)

    def test_projects_status_as_semantic_type_without_exposing_header_or_label_content(self):
        values = ["classe_privada_a"] * 5 + ["classe_privada_b"] * 5
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Status",
            values=values,
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertIn("status_candidate", [item["semantic_type"] for item in diagnosis["semantic_classifications"]])
        self.assertTrue(any(question["blocking"] for question in diagnosis["questions"]))
        self.assertNotIn("Status", serialized)
        self.assertNotIn("classe_privada_a", serialized)

    def test_projects_category_as_semantic_type_without_exposing_header_or_label_content(self):
        values = ["categoria_privada_a"] * 5 + ["categoria_privada_b"] * 5
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Categoria",
            values=values,
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertIn("category_candidate", [item["semantic_type"] for item in diagnosis["semantic_classifications"]])
        self.assertTrue(any(question["blocking"] for question in diagnosis["questions"]))
        self.assertNotIn("Categoria", serialized)
        self.assertNotIn("categoria_privada_a", serialized)

    def test_projects_location_as_semantic_type_without_exposing_header_or_label_content(self):
        values = ["local_privado_a"] * 5 + ["local_privado_b"] * 5
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Cidade",
            values=values,
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertIn("location_candidate", [item["semantic_type"] for item in diagnosis["semantic_classifications"]])
        self.assertTrue(any(question["blocking"] for question in diagnosis["questions"]))
        self.assertNotIn("Cidade", serialized)
        self.assertNotIn("local_privado_a", serialized)

    def test_projects_responsible_as_semantic_type_without_exposing_header_or_label_content(self):
        values = ["responsavel_privado_a"] * 5 + ["responsavel_privado_b"] * 5
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Responsável",
            values=values,
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )

        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        serialized = json.dumps(diagnosis)

        self.assertIn("responsible_candidate", [item["semantic_type"] for item in diagnosis["semantic_classifications"]])
        self.assertTrue(any(question["blocking"] for question in diagnosis["questions"]))
        self.assertNotIn("Responsável", serialized)
        self.assertNotIn("responsavel_privado_a", serialized)

    def test_schema_rejects_unknown_root_property_and_preserves_question_lineage_per_sheet(self):
        sales = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Total",
            values=["10", "20"],
            sheet_name="Vendas",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )
        costs = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000020",
            column_id="00000000-0000-4000-8000-000000000021",
            column_name="Custo",
            values=["30", "40"],
            sheet_name="Custos",
            sheet_position=1,
            sheet_visibility="visible",
            column_position=0,
        )
        diagnosis = execute_quality_diagnosis([sales, costs], metadata=METADATA)

        self.assertEqual(len(diagnosis["questions"]), 2)
        self.assertTrue(all(len(sheet["question_ids"]) == 1 for sheet in diagnosis["sheets"]))
        invalid = copy.deepcopy(diagnosis)
        invalid["unexpected_property"] = True
        with self.assertRaises(ValueError):
            validate_diagnosis_root(invalid)

    def test_executor_uses_metadata_and_context_instead_of_generic_operational_values(self):
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Valor",
            values=["10", "20"],
            sheet_name="Dados ocultos",
            sheet_position=3,
            sheet_visibility="hidden",
            column_position=2,
        )
        metadata = replace(
            METADATA,
            domain="hr",
            file_mime_type="application/custom-xlsx",
            retention_status="retention-policy-a",
            terms_version="2026.08",
            analysis_version=4,
            execution_profile=replace(METADATA.execution_profile, engine_version="0.1.0-test", ruleset_version="0.7.0-test"),
        )

        diagnosis = execute_quality_diagnosis([context], metadata=metadata)

        self.assertEqual(diagnosis["analysis"]["domain"], "hr")
        self.assertEqual(diagnosis["analysis"]["version"], 4)
        self.assertEqual(diagnosis["analysis"]["terms_version"], "2026.08")
        self.assertEqual(diagnosis["file"]["mime_type"], "application/custom-xlsx")
        self.assertEqual(diagnosis["file"]["retention"]["status"], "retention-policy-a")
        self.assertEqual(diagnosis["sheets"][0]["visibility"], "hidden")
        self.assertEqual(diagnosis["summary"]["completeness_ratio"], round(executable_rule_count() / metadata.execution_profile.catalog_target_rule_count, 8))
        self.assertEqual(diagnosis["execution"]["engine_version"], "0.1.0-test")
        self.assertEqual(diagnosis["execution"]["ruleset_version"], "0.7.0-test")

    def test_executor_propagates_all_governed_profile_markers_without_internal_fallbacks(self):
        profile = replace(
            METADATA.execution_profile,
            engine_version="engine-from-profile",
            ruleset_version="ruleset-from-profile",
            confidence_methodology_version="confidence-from-profile",
            execution_status="execution-from-profile",
            module_name="module-from-profile",
            module_status="module-status-from-profile",
            ai_usage={"used": False, "providers": ["profile-only"], "fallback": "profile-fallback"},
            assumption="assumption-from-profile",
            limitation="limitation-from-profile",
            proposed_model_status="hypothesis",
            proposed_model_limitation="model-limitation-from-profile",
            summary_template="summary:{sheet_count}:{column_count}:{finding_count}",
            next_action_with_questions="action-with-question-from-profile",
            next_action_without_questions="action-without-question-from-profile",
        )
        metadata = replace(METADATA, execution_profile=profile)
        context_with_question = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000010",
            column_id="00000000-0000-4000-8000-000000000011",
            column_name="Valor",
            values=["10", "20"],
            sheet_name="Vendas",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )
        diagnosis_with_question = execute_quality_diagnosis([context_with_question], metadata=metadata)

        self.assertEqual(diagnosis_with_question["analysis"]["assumptions"], ["assumption-from-profile"])
        self.assertEqual(diagnosis_with_question["analysis"]["limitations"], ["limitation-from-profile"])
        self.assertEqual(diagnosis_with_question["summary"]["executive_summary"], "summary:1:1:1")
        self.assertEqual(diagnosis_with_question["summary"]["next_recommended_action"], "action-with-question-from-profile")
        self.assertEqual(diagnosis_with_question["proposed_model"]["status"], "hypothesis")
        self.assertEqual(diagnosis_with_question["proposed_model"]["limitations"], ["model-limitation-from-profile"])
        self.assertEqual(diagnosis_with_question["execution"]["engine_version"], "engine-from-profile")
        self.assertEqual(diagnosis_with_question["execution"]["ruleset_version"], "ruleset-from-profile")
        self.assertEqual(diagnosis_with_question["execution"]["confidence_methodology_version"], "confidence-from-profile")
        self.assertEqual(diagnosis_with_question["execution"]["status"], "execution-from-profile")
        self.assertEqual(diagnosis_with_question["execution"]["modules"][0]["module"], "module-from-profile")
        self.assertEqual(diagnosis_with_question["execution"]["modules"][0]["status"], "module-status-from-profile")
        self.assertEqual(diagnosis_with_question["execution"]["ai_usage"], {"used": False, "providers": ["profile-only"], "fallback": "profile-fallback"})

        context_without_question = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000020",
            column_id="00000000-0000-4000-8000-000000000021",
            column_name="Descrição",
            values=["texto", "outro"],
            sheet_name="Descrições",
            sheet_position=1,
            sheet_visibility="visible",
            column_position=0,
        )
        diagnosis_without_question = execute_quality_diagnosis([context_without_question], metadata=metadata)
        self.assertEqual(diagnosis_without_question["summary"]["next_recommended_action"], "action-without-question-from-profile")
