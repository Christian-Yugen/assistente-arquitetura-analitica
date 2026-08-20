"""Profiling agregado de ausência para a QLT-NULL-001 reconstruída."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class MissingnessProfile:
    """Contagens determinísticas de ausência, sem valores brutos."""

    observed_cell_count: int = 0
    non_missing_cell_count: int = 0
    structural_null_count: int = 0
    blank_text_count: int = 0
    numeric_nan_count: int = 0

    @property
    def missing_cell_count(self) -> int:
        return self.structural_null_count + self.blank_text_count + self.numeric_nan_count

    @property
    def missing_ratio(self) -> float:
        return round(self.missing_cell_count / self.observed_cell_count, 8) if self.observed_cell_count else 0.0

    @property
    def missing_class_count(self) -> int:
        return sum(count > 0 for count in (self.structural_null_count, self.blank_text_count, self.numeric_nan_count))


def missing_class(value: object) -> str | None:
    """Classifica somente as ausências determinísticas aprovadas pela política."""

    if value is None:
        return "structural_null"
    if isinstance(value, str) and not value.strip():
        return "blank_text"
    if isinstance(value, float) and math.isnan(value):
        return "numeric_nan"
    return None


def row_has_meaningful_value(values: tuple[object, ...] | list[object]) -> bool:
    """Exclui linhas inteiramente ausentes sem inspecionar nem reter conteúdo."""

    return any(missing_class(value) is None for value in values)


def profile_missingness(values: list[object]) -> MissingnessProfile:
    structural_null_count = 0
    blank_text_count = 0
    numeric_nan_count = 0
    non_missing_cell_count = 0

    for value in values:
        kind = missing_class(value)
        if kind == "structural_null":
            structural_null_count += 1
        elif kind == "blank_text":
            blank_text_count += 1
        elif kind == "numeric_nan":
            numeric_nan_count += 1
        else:
            non_missing_cell_count += 1

    return MissingnessProfile(
        observed_cell_count=len(values),
        non_missing_cell_count=non_missing_cell_count,
        structural_null_count=structural_null_count,
        blank_text_count=blank_text_count,
        numeric_nan_count=numeric_nan_count,
    )
