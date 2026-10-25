"""R2: teste XLSX -> perfilamento -> motor -> JSON, sem persistir valores brutos."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4
from openpyxl import Workbook
from engine.workbook_runner import run

class R2WorkbookIntegrationTests(unittest.TestCase):
    def _diagnose(self, duplicate=False):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(["Código do registro", "Cliente", "Categoria"])
            for index in range(175):
                identifier = None if index < 5 else f"id-{index - 5:04d}"
                if duplicate and index == 174:
                    identifier = "id-0000"
                sheet.append([identifier, f"Cliente sintético {index}", "A" if index % 2 else "B"])
            source = folder / "input.xlsx"
            workbook.save(source)
            payload = source.read_bytes()
            uid = lambda: str(uuid4())
            metadata = dict(analysis_id=uid(), project_id=uid(), owner_user_id=uid(), project_name="R2", objective="Teste", file_id=uid(), original_name="input.xlsx", file_size_bytes=len(payload), file_sha256=hashlib.sha256(payload).hexdigest(), file_mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", workbook_readable=True, consented_at="2026-10-24T00:00:00Z", created_at="2026-10-24T00:00:00Z", uploaded_at="2026-10-24T00:00:00Z", retention_delete_at="2026-10-24T00:00:00Z", retention_status="reference_removed", correlation_id=uid(), terms_version="1.0", domain="generic", business_questions=[], analysis_version=1, supersedes_analysis_id=None)
            meta = folder / "metadata.json"
            meta.write_text(json.dumps(metadata), encoding="utf-8")
            return run(source, meta)

    def test_valid_subset_produces_explicit_grain_and_preserves_quality_finding(self):
        diagnosis = self._diagnose()
        self.assertEqual(diagnosis["proposed_model"]["tables"][0]["grain_rule_id"], "GRN-EXPL-002")
        self.assertTrue(any(q["impact"]["affected_rule_ids"] == ["GRN-EXPL-002"] and q["blocking"] for q in diagnosis["questions"]))
        self.assertTrue(any(f["rule_id"] == "QLT-NULL-001" for f in diagnosis["findings"]))
        self.assertNotIn("Cliente sintético 174", json.dumps(diagnosis, ensure_ascii=False))

    def test_duplicate_in_eligible_subset_blocks_explicit_grain(self):
        diagnosis = self._diagnose(duplicate=True)
        self.assertNotEqual(diagnosis["proposed_model"]["tables"][0]["grain_rule_id"], "GRN-EXPL-002")
