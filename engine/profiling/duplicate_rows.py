"""Profiling agregado de linhas tecnicamente repetidas, sem reter conteúdo do workbook."""

from __future__ import annotations

import math
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable, Sequence

from engine.profiling.missingness import row_has_meaningful_value


NORMALIZATION_BASIS = "type_tagged_nfkc_trim_newlines"


@dataclass(frozen=True)
class DuplicateRowsProfile:
    non_empty_row_count: int = 0
    duplicate_group_count: int = 0
    duplicate_row_count: int = 0
    duplicate_row_ratio: float = 0.0
    largest_duplicate_group: int = 0
    normalization_basis: str = NORMALIZATION_BASIS


def _text_signature(value: str) -> str:
    """Aplica somente a normalização técnica aprovada, sem aproximar significado."""

    return unicodedata.normalize("NFKC", value).replace("\r\n", "\n").replace("\r", "\n").strip()


def _cell_signature(value: object) -> tuple[str, str]:
    """Distingue tipos para evitar colidir, por exemplo, texto '1' e número 1."""

    if value is None:
        return ("null", "")
    if isinstance(value, bool):
        return ("boolean", str(value).lower())
    if isinstance(value, str):
        return ("text", _text_signature(value))
    if isinstance(value, int):
        return ("integer", str(value))
    if isinstance(value, float):
        if math.isnan(value):
            return ("numeric_nan", "")
        return ("float", repr(value))
    if isinstance(value, datetime):
        return ("datetime", value.isoformat())
    if isinstance(value, date):
        return ("date", value.isoformat())
    return (type(value).__name__, repr(value))


class DuplicateRowsAccumulator:
    """Acumula somente assinaturas efêmeras durante a leitura de uma aba."""

    def __init__(self) -> None:
        self._counts: Counter[tuple[tuple[str, str], ...]] = Counter()
        self._non_empty_row_count = 0

    def consume(self, row: Sequence[object]) -> None:
        if not row_has_meaningful_value(row):
            return
        self._non_empty_row_count += 1
        self._counts[tuple(_cell_signature(value) for value in row)] += 1

    def finalize(self) -> DuplicateRowsProfile:
        duplicate_sizes = [count for count in self._counts.values() if count >= 2]
        duplicate_row_count = sum(duplicate_sizes)
        result = DuplicateRowsProfile(
            non_empty_row_count=self._non_empty_row_count,
            duplicate_group_count=len(duplicate_sizes),
            duplicate_row_count=duplicate_row_count,
            duplicate_row_ratio=round(duplicate_row_count / self._non_empty_row_count, 8) if self._non_empty_row_count else 0.0,
            largest_duplicate_group=max(duplicate_sizes, default=0),
        )
        self._counts.clear()
        return result


def profile_duplicate_rows(rows: Iterable[Sequence[object]]) -> DuplicateRowsProfile:
    accumulator = DuplicateRowsAccumulator()
    for row in rows:
        accumulator.consume(row)
    return accumulator.finalize()
