"""Perfil agregado para possíveis linhas totalizadoras por aba."""

from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass
from typing import Iterable

from engine.profiling.missingness import row_has_meaningful_value


NORMALIZATION_BASIS = "first_significant_label_exact_ptbr_total_terms_with_physical_numeric_peer_after_three_non_empty_rows"
TOTAL_LABELS = frozenset({"total", "subtotal", "total geral"})


@dataclass(frozen=True)
class TotalRowsProfile:
    non_empty_row_count: int = 0
    total_row_candidate_count: int = 0
    total_row_candidate_ratio: float = 0.0
    normalization_basis: str = NORMALIZATION_BASIS


def _first_meaningful_value(row: tuple[object, ...]) -> object | None:
    for value in row:
        if row_has_meaningful_value((value,)):
            return value
    return None


def _is_authorized_label(value: object | None) -> bool:
    if not isinstance(value, str):
        return False
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    return normalized in TOTAL_LABELS


def _is_physical_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return not (isinstance(value, float) and math.isnan(value))


def _has_numeric_peer(row: tuple[object, ...], first_value: object) -> bool:
    skipped_first = False
    for value in row:
        if not skipped_first and value is first_value:
            skipped_first = True
            continue
        if _is_physical_number(value):
            return True
    return False


@dataclass
class TotalRowsAccumulator:
    """Conta candidatos sem reter rótulos, valores, fórmulas ou posições."""

    non_empty_row_count: int = 0
    total_row_candidate_count: int = 0

    def consume(self, row: tuple[object, ...]) -> None:
        if not row_has_meaningful_value(row):
            return
        first_value = _first_meaningful_value(row)
        if (
            self.non_empty_row_count >= 3
            and _is_authorized_label(first_value)
            and _has_numeric_peer(row, first_value)
        ):
            self.total_row_candidate_count += 1
        self.non_empty_row_count += 1

    def finalize(self) -> TotalRowsProfile:
        ratio = self.total_row_candidate_count / self.non_empty_row_count if self.non_empty_row_count else 0.0
        return TotalRowsProfile(
            non_empty_row_count=self.non_empty_row_count,
            total_row_candidate_count=self.total_row_candidate_count,
            total_row_candidate_ratio=round(ratio, 8),
        )


def profile_total_rows(rows: Iterable[tuple[object, ...]]) -> TotalRowsProfile:
    accumulator = TotalRowsAccumulator()
    for row in rows:
        accumulator.consume(row)
    return accumulator.finalize()
