"""Validação e normalização temporária de CSV para o profiler de workbook."""

from __future__ import annotations

import csv
import io
import math
import re
from datetime import date
from pathlib import Path
from typing import Iterator

from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell

MAX_CSV_COLUMNS = 512
MAX_CSV_ROWS = 250_000
ALLOWED_DELIMITERS = (",", ";", "\t")
_CANONICAL_NUMBER = re.compile(r"^-?(?:0|[1-9]\d*)(?:\.\d+)?$")
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class CsvWorkbookError(ValueError):
    """Falha fechada para CSV que não cumpre o contrato draft."""


def _read_text(path: Path) -> str:
    raw = path.read_bytes()
    if not raw:
        raise CsvWorkbookError("O CSV está vazio.")
    if b"\x00" in raw:
        raise CsvWorkbookError("O CSV contém bytes binários não permitidos.")
    try:
        return raw.decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError as error:
        raise CsvWorkbookError("O CSV deve usar codificação UTF-8.") from error


def _candidate_delimiters(text: str) -> list[str]:
    sample = "\n".join(line for line in text.splitlines() if line.strip())[:65_536]
    if not sample:
        raise CsvWorkbookError("O CSV não possui cabeçalho analisável.")

    scored: list[tuple[int, int, str]] = []
    malformed_structured_delimiter = False
    for priority, delimiter in enumerate(ALLOWED_DELIMITERS):
        try:
            rows = list(csv.reader(io.StringIO(sample), delimiter=delimiter, strict=True))
        except csv.Error:
            continue
        non_empty = [row for row in rows if any(cell.strip() for cell in row)]
        if not non_empty:
            continue
        widths = [len(row) for row in non_empty]
        header_width = widths[0]
        if header_width > MAX_CSV_COLUMNS:
            continue
        if header_width > 1 and len(set(widths)) != 1:
            malformed_structured_delimiter = True
            continue
        if len(set(widths)) != 1:
            continue
        scored.append((header_width, -priority, delimiter))

    if malformed_structured_delimiter:
        raise CsvWorkbookError("O CSV possui linhas com quantidade divergente de campos.")
    if not scored:
        raise CsvWorkbookError("O CSV não possui delimitador ou estrutura de linhas permitidos.")
    return [max(scored)[2]]


def iter_csv_rows(path: Path) -> Iterator[list[str]]:
    text = _read_text(path)
    delimiter = _candidate_delimiters(text)[0]
    try:
        reader = csv.reader(io.StringIO(text), delimiter=delimiter, strict=True)
        expected_width: int | None = None
        row_count = 0
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            if expected_width is None:
                expected_width = len(row)
                if expected_width == 0 or expected_width > MAX_CSV_COLUMNS:
                    raise CsvWorkbookError("O CSV não possui cabeçalho permitido.")
            elif len(row) != expected_width:
                raise CsvWorkbookError("O CSV possui linhas com quantidade divergente de campos.")
            row_count += 1
            if row_count - 1 > MAX_CSV_ROWS:
                raise CsvWorkbookError("O CSV excede o limite de 250.000 registros.")
            yield row
    except csv.Error as error:
        raise CsvWorkbookError("O CSV possui aspas ou delimitadores inválidos.") from error


def inspect_csv(path: Path) -> dict[str, int]:
    rows = iter_csv_rows(path)
    header = next(rows, None)
    if header is None or not any(cell.strip() for cell in header):
        raise CsvWorkbookError("O CSV deve conter uma linha de cabeçalho não vazia.")
    return {"sheet_count": 1}


def _typed_value(raw: str) -> object | None:
    value = raw.strip()
    if not value:
        return None
    if _CANONICAL_NUMBER.fullmatch(value):
        number = float(value) if "." in value else int(value)
        if math.isfinite(number):
            return number
    if _ISO_DATE.fullmatch(value):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    return raw


def convert_csv_to_workbook(input_path: Path, output_path: Path) -> None:
    rows = iter_csv_rows(input_path)
    header = next(rows, None)
    if header is None or not any(cell.strip() for cell in header):
        raise CsvWorkbookError("O CSV deve conter uma linha de cabeçalho não vazia.")

    workbook = Workbook(write_only=True)
    worksheet = workbook.create_sheet(title="Dados CSV")
    for row in [header, *rows]:
        cells = []
        for raw in row:
            value = _typed_value(raw)
            cell = WriteOnlyCell(worksheet, value=value)
            if isinstance(value, str):
                cell.data_type = "s"
            cells.append(cell)
        worksheet.append(cells)
    workbook.save(output_path)
