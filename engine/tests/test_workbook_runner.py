import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from openpyxl import Workbook

from engine.profiling.workbook import WorkbookValidationError
from engine.workbook_runner import run, safe_engine_failure_code


class WorkbookRunnerTests(unittest.TestCase):
    def test_classifies_exceptions_with_an_allowlisted_failure_code_only(self):
        self.assertEqual(safe_engine_failure_code(WorkbookValidationError("conteúdo privado")), "engine_workbook_invalid")
        self.assertEqual(safe_engine_failure_code(ValueError("conteúdo privado")), "engine_value_error")
        self.assertEqual(safe_engine_failure_code(TypeError("conteúdo privado")), "engine_type_error")
        self.assertEqual(safe_engine_failure_code(RuntimeError("conteúdo privado")), "engine_unexpected_error")

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
