"""Profiling agregado de coexistência de tipos físicos por coluna."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable

from engine.profiling.missingness import missing_class
from engine.profiling.numeric_text import STRICT_CANONICAL_NUMBER


NORMALIZATION_BASIS = "missingness_excluded__strict_canonical_numeric_text_delegated__python_physical_groups_v1"


@dataclass(frozen=True)
class MixedTypesProfile:
    """Contagens agregadas por grupo físico, sem valores ou posições de célula."""

    non_empty_value_count: int = 0
    boolean_count: int = 0
    numeric_count: int = 0
    text_non_numeric_count: int = 0
    temporal_count: int = 0
    strict_numeric_text_count: int = 0
    unsupported_count: int = 0
    normalization_basis: str = NORMALIZATION_BASIS

    def group_counts(self) -> tuple[tuple[str, int], ...]:
        return (
            ("boolean", self.boolean_count),
            ("numeric", self.numeric_count),
            ("text", self.text_non_numeric_count),
            ("temporal", self.temporal_count),
        )


class MixedTypesAccumulator:
    """Acumula apenas a distribuição física autorizada para a regra."""

    def __init__(self) -> None:
        self._non_empty_value_count = 0
        self._boolean_count = 0
        self._numeric_count = 0
        self._text_non_numeric_count = 0
        self._temporal_count = 0
        self._strict_numeric_text_count = 0
        self._unsupported_count = 0

    def consume(self, value: object) -> None:
        if missing_class(value) is not None:
            return
        self._non_empty_value_count += 1
        if isinstance(value, bool):
            self._boolean_count += 1
            return
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            self._numeric_count += 1
            return
        if isinstance(value, str):
            if STRICT_CANONICAL_NUMBER.fullmatch(value.strip()):
                self._strict_numeric_text_count += 1
            else:
                self._text_non_numeric_count += 1
            return
        if isinstance(value, (datetime, date)):
            self._temporal_count += 1
            return
        self._unsupported_count += 1

    def finalize(self) -> MixedTypesProfile:
        return MixedTypesProfile(
            non_empty_value_count=self._non_empty_value_count,
            boolean_count=self._boolean_count,
            numeric_count=self._numeric_count,
            text_non_numeric_count=self._text_non_numeric_count,
            temporal_count=self._temporal_count,
            strict_numeric_text_count=self._strict_numeric_text_count,
            unsupported_count=self._unsupported_count,
        )


def profile_mixed_types(values: Iterable[object]) -> MixedTypesProfile:
    accumulator = MixedTypesAccumulator()
    for value in values:
        accumulator.consume(value)
    return accumulator.finalize()
