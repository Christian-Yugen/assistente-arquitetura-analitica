import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4
from unittest.mock import patch

from openpyxl import Workbook

from engine.alerts.quality import CriticalQualityRiskProfile, classify_critical_quality_risk
from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.pipeline.quality_diagnosis import DiagnosisMetadata, build_column_analysis_context, execute_quality_diagnosis
from engine.profiling.workbook import WorkbookValidationError
from engine.workbook_runner import run, safe_engine_failure_code


class WorkbookRunnerTests(unittest.TestCase):
    def test_classifies_exceptions_with_an_allowlisted_failure_code_only(self):
        self.assertEqual(safe_engine_failure_code(WorkbookValidationError("conteúdo privado")), "engine_workbook_invalid")
        self.assertEqual(safe_engine_failure_code(ValueError("conteúdo privado")), "engine_value_error")
        self.assertEqual(safe_engine_failure_code(TypeError("conteúdo privado")), "engine_type_error")
        self.assertEqual(safe_engine_failure_code(RuntimeError("conteúdo privado")), "engine_unexpected_error")

    def test_completes_model_level_alert_without_assigning_it_to_a_workbook_sheet(self):
        model_alert = classify_critical_quality_risk(
            CriticalQualityRiskProfile(high_quality_finding_count=3, distinct_quality_rule_count=2, analyzed_sheet_count=1)
        )
        self.assertIsNotNone(model_alert)
        original_execute = __import__("engine.pipeline.quality_diagnosis", fromlist=["execute_registered_rule"]).execute_registered_rule

        def execute_with_model_alert(rule_id, profile):
            if rule_id == "ALT-QUALITY-002":
                return model_alert
            return original_execute(rule_id, profile)

        metadata = DiagnosisMetadata(
            analysis_id=str(uuid4()), project_id=str(uuid4()), owner_user_id=str(uuid4()), project_name="Teste", objective="Validar alerta global",
            file_id=str(uuid4()), original_name="entrada.xlsx", file_size_bytes=0, file_sha256="0" * 64,
            file_mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", workbook_readable=True,
            consented_at="2026-08-20T00:00:00Z", created_at="2026-08-20T00:00:00Z", uploaded_at="2026-08-20T00:00:00Z",
            retention_delete_at="2026-08-20T00:00:00Z", retention_status="reference_removed", correlation_id=str(uuid4()),
            terms_version="1.0", domain="generic", business_questions=(), analysis_version=1, supersedes_analysis_id=None,
            execution_profile=load_authorized_draft_profile(),
        )
        context = build_column_analysis_context(
            sheet_id=str(uuid4()), column_id=str(uuid4()), column_name="Coluna 1", values=[1, 2, 3],
            sheet_name="Aba 1", sheet_position=0, sheet_visibility="visible", column_position=0,
        )

        with patch("engine.pipeline.quality_diagnosis.execute_registered_rule", side_effect=execute_with_model_alert):
            diagnosis = execute_quality_diagnosis([context], metadata=metadata)

        alert_finding = next(finding for finding in diagnosis["findings"] if finding["rule_id"] == "ALT-QUALITY-002")
        self.assertEqual(alert_finding["affected_entities"], [{"entity_type": "model", "entity_id": "model"}])
        self.assertTrue(any(question["impact"]["affected_rule_ids"] == ["ALT-QUALITY-002"] for question in diagnosis["questions"]))
        self.assertFalse(any(alert_finding["finding_id"] in sheet["finding_ids"] for sheet in diagnosis["sheets"]))

    def test_runs_validated_workbook_to_canonical_diagnosis_without_raw_values(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workbook_path = base / "entrada.xlsx"
            metadata_path = base / "metadata.json"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Vendas"
            sheet.append(["Produto", "Valor"])
            sheet.append(["Alpha", "100"])
            sheet.append(["Beta", "200"])
            workbook.save(workbook_path)
            content = workbook_path.read_bytes()
            metadata_path.write_text(json.dumps({
                "analysis_id": str(uuid4()), "project_id": str(uuid4()), "owner_user_id": str(uuid4()),
                "project_name": "Teste", "objective": "Validar runner", "file_id": str(uuid4()),
                "original_name": "entrada.xlsx", "file_size_bytes": len(content), "file_sha256": hashlib.sha256(content).hexdigest(),
                "file_mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "workbook_readable": True,
                "consented_at": "2026-08-20T00:00:00Z", "created_at": "2026-08-20T00:00:00Z",
                "uploaded_at": "2026-08-20T00:00:00Z", "retention_delete_at": "2026-08-20T00:00:00Z",
                "retention_status": "reference_removed", "correlation_id": str(uuid4()), "terms_version": "1.0",
                "domain": "generic", "business_questions": [], "analysis_version": 1, "supersedes_analysis_id": None,
            }), encoding="utf-8")

            diagnosis = run(workbook_path, metadata_path)
            serialized = json.dumps(diagnosis)

            self.assertEqual(diagnosis["contract_id"], "PM-MVP-PBI-CON-001")
            self.assertEqual(diagnosis["file"]["sheet_count"], 1)
            self.assertEqual(diagnosis["summary"]["counts"]["risks"], 1)
            self.assertNotIn("Alpha", serialized)
            self.assertNotIn("Beta", serialized)
            self.assertNotIn("raw_values", serialized)

    def test_emits_dimension_grain_and_count_metric_from_a_supported_synthetic_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workbook_path = base / "modelo_dimensao.xlsx"
            metadata_path = base / "metadata.json"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Aba sintética"
            sheet.append(["ID", "Cliente", "Categoria"])
            for position in range(1, 21):
                sheet.append([f"id-{position:03d}", f"entidade-{position}", "grupo-a" if position % 2 else "grupo-b"])
            workbook.save(workbook_path)
            content = workbook_path.read_bytes()
            metadata_path.write_text(json.dumps({
                "analysis_id": str(uuid4()), "project_id": str(uuid4()), "owner_user_id": str(uuid4()),
                "project_name": "Teste sintético", "objective": "Validar estrutura de dimensão", "file_id": str(uuid4()),
                "original_name": "modelo_dimensao.xlsx", "file_size_bytes": len(content), "file_sha256": hashlib.sha256(content).hexdigest(),
                "file_mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "workbook_readable": True,
                "consented_at": "2026-08-27T00:00:00Z", "created_at": "2026-08-27T00:00:00Z",
                "uploaded_at": "2026-08-27T00:00:00Z", "retention_delete_at": "2026-08-27T00:00:00Z",
                "retention_status": "reference_removed", "correlation_id": str(uuid4()), "terms_version": "1.0",
                "domain": "generic", "business_questions": [], "analysis_version": 1, "supersedes_analysis_id": None,
            }), encoding="utf-8")

            diagnosis = run(workbook_path, metadata_path)
            serialized = json.dumps(diagnosis)

            self.assertIsNotNone(diagnosis["sheets"][0]["grain"])
            self.assertEqual(diagnosis["sheets"][0]["classification"]["type"], "dimension_standard_candidate")
            self.assertTrue(any(metric["metric_type"] == "count_conceptual_metric_candidate" for metric in diagnosis["metrics"]))
            self.assertEqual(diagnosis["summary"]["counts"]["dimensions"], 1)
            self.assertEqual(diagnosis["summary"]["counts"]["facts"], 0)
            self.assertEqual(len(diagnosis["proposed_model"]["tables"]), 1)
            self.assertEqual(diagnosis["proposed_model"]["tables"][0]["table_type"], "dimension_standard_candidate")
            self.assertTrue(all(isinstance(option, dict) for question in diagnosis["questions"] for option in question["options"]))
            self.assertNotIn("Aba sintética", serialized)
            self.assertNotIn("entidade-001", serialized)
            self.assertNotIn("raw_values", serialized)

    def test_runs_multi_sheet_draft_workbook_to_sanitized_modeling_diagnosis(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workbook_path = base / "modelo_sintetico.xlsx"
            metadata_path = base / "metadata.json"
            workbook = Workbook()
            dimension = workbook.active
            dimension.title = "Entidades sintéticas"
            dimension.append(["Identificador interno", "Categoria interna"])
            for position in range(1, 21):
                dimension.append([f"entidade-{position}", "grupo-a" if position % 2 else "grupo-b"])
            facts = workbook.create_sheet("Eventos sintéticos")
            facts.append(["Identificador de evento", "Data do evento", "Quantidade interna", "Valor interno"])
            for position in range(1, 21):
                facts.append([f"evento-{position}", f"2026-01-{position:02d}", position, position * 10])
            workbook.save(workbook_path)
            content = workbook_path.read_bytes()
            metadata_path.write_text(json.dumps({
                "analysis_id": str(uuid4()), "project_id": str(uuid4()), "owner_user_id": str(uuid4()),
                "project_name": "Teste sintético", "objective": "Validar fluxo multissheet", "file_id": str(uuid4()),
                "original_name": "modelo_sintetico.xlsx", "file_size_bytes": len(content), "file_sha256": hashlib.sha256(content).hexdigest(),
                "file_mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "workbook_readable": True,
                "consented_at": "2026-08-27T00:00:00Z", "created_at": "2026-08-27T00:00:00Z",
                "uploaded_at": "2026-08-27T00:00:00Z", "retention_delete_at": "2026-08-27T00:00:00Z",
                "retention_status": "reference_removed", "correlation_id": str(uuid4()), "terms_version": "1.0",
                "domain": "generic", "business_questions": [], "analysis_version": 1, "supersedes_analysis_id": None,
            }), encoding="utf-8")

            diagnosis = run(workbook_path, metadata_path)
            serialized = json.dumps(diagnosis)

            self.assertEqual(diagnosis["contract_id"], "PM-MVP-PBI-CON-001")
            self.assertEqual(diagnosis["file"]["sheet_count"], 2)
            self.assertEqual(diagnosis["execution"]["status"], "completed")
            self.assertIn("semantic_classifications", diagnosis)
            self.assertIn("relationships", diagnosis)
            self.assertIn("metrics", diagnosis)
            self.assertNotIn("Entidades sintéticas", serialized)
            self.assertNotIn("Eventos sintéticos", serialized)
            self.assertNotIn("Identificador interno", serialized)
            self.assertNotIn("evento-1", serialized)
            self.assertNotIn("raw_values", serialized)

    def test_runs_missingness_workbook_to_reconstructed_null_finding_without_raw_values(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workbook_path = base / "entrada_nulos.xlsx"
            metadata_path = base / "metadata.json"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Dados privados"
            sheet.append(["Observação", "Referência"])
            for position in range(16):
                sheet.append(["conteúdo confidencial", f"REF-{position}"])
            for position in range(4):
                sheet.append([None, f"AUS-{position}"])
            workbook.save(workbook_path)
            content = workbook_path.read_bytes()
            metadata_path.write_text(json.dumps({
                "analysis_id": str(uuid4()), "project_id": str(uuid4()), "owner_user_id": str(uuid4()),
                "project_name": "Teste", "objective": "Validar runner", "file_id": str(uuid4()),
                "original_name": "entrada_nulos.xlsx", "file_size_bytes": len(content), "file_sha256": hashlib.sha256(content).hexdigest(),
                "file_mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "workbook_readable": True,
                "consented_at": "2026-08-20T00:00:00Z", "created_at": "2026-08-20T00:00:00Z",
                "uploaded_at": "2026-08-20T00:00:00Z", "retention_delete_at": "2026-08-20T00:00:00Z",
                "retention_status": "reference_removed", "correlation_id": str(uuid4()), "terms_version": "1.0",
                "domain": "generic", "business_questions": [], "analysis_version": 1, "supersedes_analysis_id": None,
            }), encoding="utf-8")

            diagnosis = run(workbook_path, metadata_path)
            serialized = json.dumps(diagnosis)
            null_findings = [finding for finding in diagnosis["findings"] if finding["rule_id"] == "QLT-NULL-001"]

            self.assertEqual(len(null_findings), 1)
            self.assertEqual(null_findings[0]["severity"], "high")
            self.assertEqual(null_findings[0]["rule_version"], "0.1.0-reconstructed.1")
            self.assertEqual(diagnosis["questions"][0]["impact"]["affected_rule_ids"], ["QLT-NULL-001"])
            self.assertNotIn("conteúdo confidencial", serialized)
            self.assertNotIn("REF-0", serialized)
            self.assertNotIn("raw_values", serialized)

    def test_masks_all_workbook_headers_before_serializing_the_diagnosis(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workbook_path = base / "entrada_cabecalhos.xlsx"
            metadata_path = base / "metadata.json"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Dados internos"
            sheet.append(["Name: Customer", "E-mail de contato", "Receita mensal"])
            for position in range(12):
                sheet.append([f"cliente-{position}", f"contato-{position}@example.test", position * 10])
            workbook.save(workbook_path)
            content = workbook_path.read_bytes()
            metadata_path.write_text(json.dumps({
                "analysis_id": str(uuid4()), "project_id": str(uuid4()), "owner_user_id": str(uuid4()),
                "project_name": "Teste", "objective": "Validar mascaramento", "file_id": str(uuid4()),
                "original_name": "entrada_cabecalhos.xlsx", "file_size_bytes": len(content), "file_sha256": hashlib.sha256(content).hexdigest(),
                "file_mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "workbook_readable": True,
                "consented_at": "2026-08-20T00:00:00Z", "created_at": "2026-08-20T00:00:00Z",
                "uploaded_at": "2026-08-20T00:00:00Z", "retention_delete_at": "2026-08-20T00:00:00Z",
                "retention_status": "reference_removed", "correlation_id": str(uuid4()), "terms_version": "1.0",
                "domain": "generic", "business_questions": [], "analysis_version": 1, "supersedes_analysis_id": None,
            }), encoding="utf-8")

            diagnosis = run(workbook_path, metadata_path)
            serialized = json.dumps(diagnosis)

            self.assertIn("Coluna 1", serialized)
            self.assertNotIn("Name: Customer", serialized)
            self.assertNotIn("E-mail de contato", serialized)
            self.assertNotIn("Receita mensal", serialized)
            self.assertNotIn("cliente-0", serialized)
            self.assertNotIn("contato-0@example.test", serialized)
