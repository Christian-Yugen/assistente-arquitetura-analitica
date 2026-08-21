import json
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from engine.profiling.workbook import profile_workbook


class SemanticCurrencyWorkbookProfilingTests(unittest.TestCase):
    def test_reduces_currency_format_metadata_to_private_aggregate_counts(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Aba Financeira Reservada"
        worksheet.append(["Receita"])
        for index in range(10):
            cell = worksheet.cell(row=index + 2, column=1, value=98765.43 + index)
            cell.number_format = "R$ #,##0.00"

        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "currency.xlsx"
            workbook.save(path)
            context = profile_workbook(path)[0]

        profile = context.semantic_currency
        serialized = json.dumps(profile.__dict__)
        self.assertTrue(profile.header_eligible)
        self.assertEqual(profile.physical_numeric_count, 10)
        self.assertEqual(profile.currency_format_numeric_count, 10)
        self.assertNotIn("R$", serialized)
        self.assertNotIn("98765", serialized)
        self.assertNotIn("Aba Financeira Reservada", serialized)
