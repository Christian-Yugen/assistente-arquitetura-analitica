import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from engine.profiling.workbook import profile_workbook


class NullWorkbookProfilingTests(unittest.TestCase):
    def test_counts_missingness_on_meaningful_rows_and_excludes_trailing_blank_rows(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(["Observação", "Referência"])
        worksheet.append([None, "A"])
        worksheet.append(["   ", "B"])
        worksheet.append(["preenchido", "C"])
        worksheet.append([None, None])

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "entrada.xlsx"
            workbook.save(path)
            contexts = profile_workbook(path)

        observation = contexts[0]
        self.assertEqual(observation.missingness.observed_cell_count, 3)
        self.assertEqual(observation.missingness.structural_null_count, 1)
        self.assertEqual(observation.missingness.blank_text_count, 1)
        self.assertEqual(observation.missingness.non_missing_cell_count, 1)
        self.assertEqual(observation.missingness.missing_ratio, 0.66666667)
        self.assertFalse(hasattr(observation.missingness, "raw_values"))


if __name__ == "__main__":
    unittest.main()
