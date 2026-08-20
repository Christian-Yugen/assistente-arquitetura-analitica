import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from engine.profiling.workbook import WorkbookValidationError, profile_workbook
from engine.workbook_validator import inspect_workbook


class WorkbookProfilingTests(unittest.TestCase):
    def create_workbook(self, sheets: int = 1) -> Path:
        handle = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        handle.close()
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Vendas"
        worksheet.append(["Cliente", "Valor", "E-mail"])
        worksheet.append(["Ana", "100", "ana@example.test"])
        worksheet.append(["Bia", "200", "bia@example.test"])
        for index in range(1, sheets):
            extra = workbook.create_sheet(f"Aba {index}")
            extra.append(["Campo"])
            extra.append(["valor"])
        workbook.save(handle.name)
        return Path(handle.name)

    def test_profiles_contexts_without_retaining_cell_values_or_sensitive_headers(self):
        path = self.create_workbook()
        try:
            contexts = profile_workbook(path)
        finally:
            path.unlink(missing_ok=True)

        value_column = next(context for context in contexts if context.column_name == "Valor")
        email_column = next(context for context in contexts if context.column_position == 2)
        self.assertEqual(len(contexts), 3)
        self.assertEqual(value_column.numeric_text.numeric_text_candidate_count, 2)
        self.assertEqual(value_column.numeric_text.numeric_text_candidate_ratio, 1.0)
        self.assertEqual(email_column.column_name, "Campo sensível 3")
        self.assertEqual({context.sheet_name for context in contexts}, {"Aba 1"})
        self.assertNotIn("Vendas", {context.sheet_name for context in contexts})
        self.assertFalse(hasattr(value_column, "raw_values"))

    def test_rejects_workbook_with_more_than_ten_sheets(self):
        path = self.create_workbook(sheets=11)
        try:
            with self.assertRaises(WorkbookValidationError):
                profile_workbook(path)
        finally:
            path.unlink(missing_ok=True)

    def test_pre_persistence_inspection_reports_valid_sheet_count(self):
        path = self.create_workbook(sheets=2)
        try:
            self.assertEqual(inspect_workbook(path), {"sheet_count": 2})
        finally:
            path.unlink(missing_ok=True)
