import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from engine.workbook_validator import WorkbookValidationError, inspect_workbook


class WorkbookValidatorTests(unittest.TestCase):
    def test_accepts_a_readable_synthetic_xlsx_within_the_sheet_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            workbook_path = Path(directory) / "synthetic.xlsx"
            workbook = Workbook()
            workbook.active.append(["field"])
            workbook.active.append(["value"])
            workbook.save(workbook_path)

            self.assertEqual(inspect_workbook(workbook_path), {"sheet_count": 1})

    def test_rejects_a_readable_workbook_above_the_sheet_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            workbook_path = Path(directory) / "too_many_sheets.xlsx"
            workbook = Workbook()
            for position in range(10):
                workbook.create_sheet(f"Sheet {position + 2}")
            workbook.save(workbook_path)

            with self.assertRaisesRegex(WorkbookValidationError, "entre 1 e 10 abas"):
                inspect_workbook(workbook_path)

    def test_rejects_unreadable_content_with_a_safe_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            workbook_path = Path(directory) / "invalid.xlsx"
            workbook_path.write_bytes(b"not an xlsx workbook")

            with self.assertRaisesRegex(WorkbookValidationError, "inválido, criptografado ou não legível"):
                inspect_workbook(workbook_path)
