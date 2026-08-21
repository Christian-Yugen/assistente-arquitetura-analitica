import json
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from engine.profiling.workbook import profile_workbook


class FormulaWorkbookProfilingTests(unittest.TestCase):
    def test_profiles_formula_types_without_retaining_formula_text_or_manual_values(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Aba Reservada"
        worksheet.append(["Resultado"])
        for index in range(1, 20):
            worksheet.append([f"=SUM({index},1)"])
        worksheet.append([98765])

        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "formulas.xlsx"
            workbook.save(path)
            contexts = profile_workbook(path)

        profile = contexts[0].formulas
        serialized = json.dumps(profile.__dict__)
        self.assertTrue(profile.eligible)
        self.assertEqual(profile.physical_nonempty_count, 20)
        self.assertEqual(profile.formula_count, 19)
        self.assertEqual(profile.nonformula_count, 1)
        self.assertNotIn("SUM", serialized)
        self.assertNotIn("98765", serialized)
        self.assertNotIn("Aba Reservada", serialized)
