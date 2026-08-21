"""Perfil agregado de presença versus ausência de fórmulas, sem reter expressões."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


FORMULA_CONSISTENCY_BASIS = "formula_presence_vs_nonformula_type_f_nonempty_min10_min8_80pct_v1"
MINIMUM_PHYSICAL_NONEMPTY_COUNT = 10
MINIMUM_FORMULA_COUNT = 8
MINIMUM_FORMULA_SHARE = 0.8


@dataclass(frozen=True)
class FormulaConsistencyProfile:
    eligible: bool = False
    physical_nonempty_count: int = 0
    formula_count: int = 0
    nonformula_count: int = 0
    nonformula_ratio: float = 0.0
    basis: str = FORMULA_CONSISTENCY_BASIS


def _is_physical_nonempty(value: object) -> bool:
    return value is not None and not (isinstance(value, str) and not value.strip())


@dataclass
class FormulaConsistencyAccumulator:
    """Acumula somente presença e tipo de célula; nunca a expressão ou o valor calculado."""

    physical_nonempty_count: int = 0
    formula_count: int = 0

    def consume(self, value: object, *, is_formula: bool) -> None:
        if not _is_physical_nonempty(value):
            return
        self.physical_nonempty_count += 1
        if is_formula:
            self.formula_count += 1

    def finalize(self) -> FormulaConsistencyProfile:
        nonformula_count = self.physical_nonempty_count - self.formula_count
        formula_ratio = self.formula_count / self.physical_nonempty_count if self.physical_nonempty_count else 0.0
        eligible = (
            self.physical_nonempty_count >= MINIMUM_PHYSICAL_NONEMPTY_COUNT
            and self.formula_count >= MINIMUM_FORMULA_COUNT
            and formula_ratio >= MINIMUM_FORMULA_SHARE
        )
        return FormulaConsistencyProfile(
            eligible=eligible,
            physical_nonempty_count=self.physical_nonempty_count,
            formula_count=self.formula_count,
            nonformula_count=nonformula_count,
            nonformula_ratio=round(nonformula_count / self.physical_nonempty_count, 8) if self.physical_nonempty_count else 0.0,
        )


def profile_formula_consistency(cells: Iterable[tuple[object, bool]]) -> FormulaConsistencyProfile:
    accumulator = FormulaConsistencyAccumulator()
    for value, is_formula in cells:
        accumulator.consume(value, is_formula=is_formula)
    return accumulator.finalize()
