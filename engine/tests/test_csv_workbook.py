from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from openpyxl import load_workbook

from engine.csv_workbook import CsvWorkbookError, convert_csv_to_workbook, inspect_csv


class CsvWorkbookTests(unittest.TestCase):
    def _path(self, content: bytes) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "input.csv"
        path.write_bytes(content)
        return path

    def test_inspects_utf8_csv_as_one_logical_sheet(self) -> None:
        path = self._path(b"id,valor\n1,10\n2,20\n")
        self.assertEqual(inspect_csv(path), {"sheet_count": 1})

    def test_supports_semicolon_delimiter(self) -> None:
        path = self._path("id;descrição\n1;ativo\n".encode("utf-8"))
        self.assertEqual(inspect_csv(path), {"sheet_count": 1})

    def test_rejects_binary_content(self) -> None:
        with self.assertRaises(CsvWorkbookError):
            inspect_csv(self._path(b"id,valor\x00\n1,2\n"))

    def test_supports_windows_1252_csv_from_local_export(self) -> None:
        path = self._path("id;descrição\n1;ativo\n".encode("cp1252"))
        self.assertEqual(inspect_csv(path), {"sheet_count": 1})

    def test_rejects_undecodable_text_content(self) -> None:
        with self.assertRaises(CsvWorkbookError):
            inspect_csv(self._path(b"id,descri\x81\n1,2\n"))

    def test_rejects_rows_with_divergent_field_counts(self) -> None:
        with self.assertRaises(CsvWorkbookError):
            inspect_csv(self._path(b"id,valor\n1,2\n3,4,5\n"))

    def test_normalizes_numbers_dates_and_formula_like_text_without_formula_execution(self) -> None:
        source = self._path(b"id,data,formula\n1,2026-08-26,=1+1\n")
        output = source.with_name("normalized.xlsx")
        convert_csv_to_workbook(source, output)
        workbook = load_workbook(output, read_only=True, data_only=False)
        row = next(workbook.active.iter_rows(min_row=2))
        self.assertEqual(row[0].value, 1)
        self.assertEqual(row[1].value.date().isoformat(), "2026-08-26")
        self.assertEqual(row[2].value, "=1+1")
        self.assertEqual(row[2].data_type, "s")
