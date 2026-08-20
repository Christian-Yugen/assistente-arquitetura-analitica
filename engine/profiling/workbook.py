"""Leitura limitada de XLSX com profiling agregado, sem persistir valores de células."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Literal
from uuid import uuid4

import pandas as pd
from openpyxl import load_workbook

from engine.pipeline.quality_diagnosis import ColumnAnalysisContext
from engine.profiling.numeric_text import LOCALE_AMBIGUOUS_NUMBER, STRICT_CANONICAL_NUMBER, NumericTextProfile


MAX_SHEETS = 10
SENSITIVE_HEADER = re.compile(r"\b(cpf|e-?mail|nome|telefone|celular|endereco|endereço)\b", re.IGNORECASE)


class WorkbookValidationError(ValueError):
    pass


@dataclass
class StreamingColumnProfiler:
    non_empty: int = 0
    bool_count: int = 0
    numeric_count: int = 0
    text_count: int = 0
    other_count: int = 0
    numeric_text_candidates: int = 0
    numeric_text_ambiguities: int = 0

    def consume(self, value: object) -> None:
        if value is None or (isinstance(value, str) and not value.strip()) or (isinstance(value, float) and pd.isna(value)):
            return
        self.non_empty += 1
        if isinstance(value, bool):
            self.bool_count += 1
            return
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            self.numeric_count += 1
            return
        if isinstance(value, str):
            self.text_count += 1
            normalized = value.strip()
            if STRICT_CANONICAL_NUMBER.fullmatch(normalized):
                self.numeric_text_candidates += 1
            elif LOCALE_AMBIGUOUS_NUMBER.fullmatch(normalized):
                self.numeric_text_ambiguities += 1
            return
        if isinstance(value, (datetime, date)):
            self.other_count += 1
            return
        self.other_count += 1

    def physical_type(self) -> str:
        kinds = sum(count > 0 for count in (self.bool_count, self.numeric_count, self.text_count, self.other_count))
        if self.non_empty == 0:
            return "unknown"
        if kinds > 1:
            return "mixed"
        if self.bool_count:
            return "boolean"
        if self.numeric_count:
            return "numeric"
        if self.text_count:
            return "text"
        return "date"

    def numeric_text_profile(self) -> NumericTextProfile:
        return NumericTextProfile(
            non_empty_value_count=self.non_empty,
            numeric_text_candidate_count=self.numeric_text_candidates,
            numeric_text_candidate_ratio=round(self.numeric_text_candidates / self.non_empty, 8) if self.non_empty else 0.0,
            numeric_text_basis="strict_canonical_numeric_string",
            numeric_text_ambiguity_count=self.numeric_text_ambiguities,
        )


def safe_column_name(value: object, position: int) -> str:
    raw = str(value).strip() if value is not None else ""
    if not raw:
        return f"Coluna {position + 1}"
    if SENSITIVE_HEADER.search(raw):
        return f"Campo sensível {position + 1}"
    return raw[:160]


def worksheet_visibility(value: str) -> Literal["visible", "hidden", "very_hidden"]:
    if value == "veryHidden":
        return "very_hidden"
    if value == "hidden":
        return "hidden"
    return "visible"


def profile_workbook(path: Path) -> list[ColumnAnalysisContext]:
    try:
        workbook = load_workbook(path, read_only=True, data_only=False, keep_links=False)
    except Exception as error:
        raise WorkbookValidationError("Arquivo XLSX inválido, criptografado ou não legível.") from error
    if len(workbook.worksheets) == 0:
        raise WorkbookValidationError("O workbook não possui abas analisáveis.")
    if len(workbook.worksheets) > MAX_SHEETS:
        raise WorkbookValidationError(f"O workbook excede o limite de {MAX_SHEETS} abas.")

    contexts: list[ColumnAnalysisContext] = []
    for sheet_position, worksheet in enumerate(workbook.worksheets):
        rows = worksheet.iter_rows(values_only=True)
        header = next(rows, None)
        if header is None:
            continue
        column_count = len(header)
        profilers = [StreamingColumnProfiler() for _ in range(column_count)]
        for row in rows:
            for position in range(column_count):
                profilers[position].consume(row[position] if position < len(row) else None)
        sheet_id = str(uuid4())
        for column_position, profiler in enumerate(profilers):
            contexts.append(
                ColumnAnalysisContext(
                    sheet_id=sheet_id,
                    sheet_name=worksheet.title[:160],
                    sheet_position=sheet_position,
                    sheet_visibility=worksheet_visibility(worksheet.sheet_state),
                    column_id=str(uuid4()),
                    column_name=safe_column_name(header[column_position], column_position),
                    column_position=column_position,
                    physical_type=profiler.physical_type(),
                    numeric_text=profiler.numeric_text_profile(),
                )
            )
    if not contexts:
        raise WorkbookValidationError("O workbook não possui colunas analisáveis após a linha de cabeçalho.")
    return contexts
