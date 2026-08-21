"""Leitura limitada de XLSX com profiling agregado, sem persistir valores de células."""

from __future__ import annotations

import math
import re
import xml.etree.ElementTree as element_tree
from dataclasses import dataclass, field
from datetime import date, datetime
from itertools import chain
from pathlib import Path
from typing import Literal
from uuid import uuid4

import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries

from engine.pipeline.quality_diagnosis import ColumnAnalysisContext
from engine.profiling.missingness import MissingnessProfile, missing_class, row_has_meaningful_value
from engine.profiling.numeric_text import LOCALE_AMBIGUOUS_NUMBER, STRICT_CANONICAL_NUMBER, NumericTextProfile
from engine.profiling.categorical_variations import CategoricalVariationProfile, profile_categorical_variations
from engine.profiling.duplicate_rows import DuplicateRowsAccumulator
from engine.profiling.empty_rows import EmptyRowsAccumulator
from engine.profiling.mixed_types import MixedTypesAccumulator
from engine.profiling.bad_dates import BadDateAccumulator
from engine.profiling.whitespace import WhitespaceAccumulator
from engine.profiling.total_rows import TotalRowsAccumulator
from engine.profiling.formula_consistency import FormulaConsistencyAccumulator
from engine.profiling.headers import profile_headers
from engine.profiling.semantic_identifier import SemanticIdentifierAccumulator, SemanticIdentifierProfile
from engine.profiling.semantic_identifier import ELIGIBLE_HEADERS, SENSITIVE_HEADERS, _normalize_header
from engine.profiling.semantic_currency import SemanticCurrencyAccumulator, has_explicit_currency_format
from engine.profiling.composite_grain import CompositeGrainAccumulator


MAX_SHEETS = 10
SENSITIVE_HEADER = re.compile(r"\b(cpf|e-?mail|nome|telefone|celular|endereco|endereço)\b", re.IGNORECASE)


class WorkbookValidationError(ValueError):
    pass


@dataclass
class StreamingColumnProfiler:
    observed: int = 0
    structural_null_count: int = 0
    blank_text_count: int = 0
    numeric_nan_count: int = 0
    non_empty: int = 0
    bool_count: int = 0
    numeric_count: int = 0
    text_count: int = 0
    other_count: int = 0
    numeric_text_candidates: int = 0
    numeric_text_ambiguities: int = 0
    mixed_types_accumulator: MixedTypesAccumulator = field(default_factory=MixedTypesAccumulator, repr=False)
    bad_dates_accumulator: BadDateAccumulator = field(default_factory=BadDateAccumulator, repr=False)
    whitespace_accumulator: WhitespaceAccumulator = field(default_factory=WhitespaceAccumulator, repr=False)
    categorical_text_values: list[str] = field(default_factory=list, repr=False)
    semantic_identifier_accumulator: SemanticIdentifierAccumulator | None = field(default=None, repr=False)

    def consume(self, value: object) -> None:
        self.observed += 1
        self.mixed_types_accumulator.consume(value)
        self.bad_dates_accumulator.consume(value)
        self.whitespace_accumulator.consume(value)
        if self.semantic_identifier_accumulator is not None:
            self.semantic_identifier_accumulator.consume(value)
        kind = missing_class(value)
        if kind == "structural_null":
            self.structural_null_count += 1
            return
        if kind == "blank_text":
            self.blank_text_count += 1
            return
        if kind == "numeric_nan":
            self.numeric_nan_count += 1
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
            self.categorical_text_values.append(normalized)
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

    def missingness_profile(self) -> MissingnessProfile:
        return MissingnessProfile(
            observed_cell_count=self.observed,
            non_missing_cell_count=self.non_empty,
            structural_null_count=self.structural_null_count,
            blank_text_count=self.blank_text_count,
            numeric_nan_count=self.numeric_nan_count,
        )

    def categorical_variation_profile(self) -> CategoricalVariationProfile:
        return profile_categorical_variations(self.categorical_text_values)

    def mixed_types_profile(self):
        return self.mixed_types_accumulator.finalize()

    def bad_dates_profile(self):
        return self.bad_dates_accumulator.finalize()

    def whitespace_profile(self):
        return self.whitespace_accumulator.finalize()

    def semantic_identifier_profile(self) -> SemanticIdentifierProfile:
        return self.semantic_identifier_accumulator.finalize() if self.semantic_identifier_accumulator else SemanticIdentifierProfile()


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


def safe_sheet_name(position: int) -> str:
    """Evita reter títulos de abas, que podem conter identificadores pessoais ou comerciais."""
    return f"Aba {position + 1}"


def _merged_ranges_for_worksheet(workbook: object, worksheet: object) -> tuple[tuple[int, int, int, int], ...]:
    """Lê apenas refs de mesclagem do XML; conteúdos e endereços não alcançam o perfil."""

    archive = getattr(workbook, "_archive", None)
    worksheet_path = getattr(worksheet, "_worksheet_path", None)
    if archive is None or not isinstance(worksheet_path, str):
        return ()
    ranges: list[tuple[int, int, int, int]] = []
    try:
        with archive.open(worksheet_path) as source:
            for _event, element in element_tree.iterparse(source, events=("end",)):
                if element.tag.endswith("mergeCell"):
                    reference = element.attrib.get("ref")
                    if reference:
                        min_col, min_row, max_col, max_row = range_boundaries(reference)
                        ranges.append((min_col, min_row, max_col, max_row))
                element.clear()
    except (KeyError, ValueError, element_tree.ParseError):
        return ()
    return tuple(ranges)


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
        rows = worksheet.iter_rows()
        header_cells = next(rows, None)
        if header_cells is None:
            continue
        second_row_cells = next(rows, None)
        header = tuple(cell.value for cell in header_cells)
        column_count = len(header)
        headers_profile = profile_headers(
            header_cells,
            second_row_cells,
            _merged_ranges_for_worksheet(workbook, worksheet),
        )
        candidate_positions = [position for position, value in enumerate(header) if _normalize_header(str(value or "")) in ELIGIBLE_HEADERS and _normalize_header(str(value or "")) not in SENSITIVE_HEADERS]
        candidate_pairs = [(candidate_positions[left], candidate_positions[right]) for left in range(len(candidate_positions)) for right in range(left + 1, len(candidate_positions))]
        composite_grain_accumulator = CompositeGrainAccumulator(candidate_pairs[:10])
        profilers = [StreamingColumnProfiler(semantic_identifier_accumulator=SemanticIdentifierAccumulator(str(header[position] or ""))) for position in range(column_count)]
        semantic_currency_accumulators = [SemanticCurrencyAccumulator(header=header[position]) for position in range(column_count)]
        formula_accumulators = [FormulaConsistencyAccumulator() for _ in range(column_count)]
        duplicate_rows_accumulator = DuplicateRowsAccumulator()
        empty_rows_accumulator = EmptyRowsAccumulator()
        total_rows_accumulator = TotalRowsAccumulator()
        data_rows = chain((second_row_cells,), rows) if second_row_cells is not None else rows
        for row in data_rows:
            bounded_cells = tuple(row[position] if position < len(row) else None for position in range(column_count))
            bounded_row = tuple(cell.value if cell is not None else None for cell in bounded_cells)
            empty_rows_accumulator.consume(bounded_row)
            total_rows_accumulator.consume(bounded_row)
            if not row_has_meaningful_value(bounded_row):
                continue
            composite_grain_accumulator.consume(bounded_row)
            duplicate_rows_accumulator.consume(bounded_row)
            for position in range(column_count):
                profilers[position].consume(bounded_row[position])
                cell = bounded_cells[position]
                semantic_currency_accumulators[position].consume(
                    bounded_row[position],
                    has_currency_format=bool(cell is not None and has_explicit_currency_format(cell.number_format)),
                )
                formula_accumulators[position].consume(
                    bounded_row[position],
                    is_formula=bool(cell is not None and cell.data_type == "f"),
                )
        duplicate_rows = duplicate_rows_accumulator.finalize()
        empty_rows = empty_rows_accumulator.finalize()
        total_rows = total_rows_accumulator.finalize()
        composite_grain = composite_grain_accumulator.finalize(eligible_pair_count=len(candidate_pairs))
        sheet_id = str(uuid4())
        for column_position, profiler in enumerate(profilers):
            categorical_variations = profiler.categorical_variation_profile()
            profiler.categorical_text_values.clear()
            contexts.append(
                ColumnAnalysisContext(
                    sheet_id=sheet_id,
                    sheet_name=safe_sheet_name(sheet_position),
                    sheet_position=sheet_position,
                    sheet_visibility=worksheet_visibility(worksheet.sheet_state),
                    column_id=str(uuid4()),
                    column_name=safe_column_name(header[column_position], column_position),
                    column_position=column_position,
                    physical_type=profiler.physical_type(),
                    numeric_text=profiler.numeric_text_profile(),
                    missingness=profiler.missingness_profile(),
                    categorical_variations=categorical_variations,
                    mixed_types=profiler.mixed_types_profile(),
                    bad_dates=profiler.bad_dates_profile(),
                    whitespace=profiler.whitespace_profile(),
                    duplicate_rows=duplicate_rows,
                    empty_rows=empty_rows,
                    total_rows=total_rows,
                    formulas=formula_accumulators[column_position].finalize(),
                    headers=headers_profile,
                    semantic_currency=semantic_currency_accumulators[column_position].finalize(),
                    semantic_identifier=profiler.semantic_identifier_profile(),
                    composite_grain=composite_grain,
                )
            )
    if not contexts:
        raise WorkbookValidationError("O workbook não possui colunas analisáveis após a linha de cabeçalho.")
    return contexts
