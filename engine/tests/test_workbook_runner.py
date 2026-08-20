import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from openpyxl import Workbook

from engine.workbook_runner import run


class WorkbookRunnerTests(unittest.TestCase):
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
