"""Sinais transitórios e opacos para a REL-ONEMANY-001.

Os conjuntos de assinaturas existem apenas durante o profiling do workbook. A
saída pública deste módulo contém somente IDs opacos e medidas agregadas.
"""

from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime

from engine.profiling.missingness import missing_class


@dataclass(frozen=True)
class RelationshipPairSignal:
    """Sinal agregado de uma direção entre colunas opacas de abas distintas."""

    source_sheet_id: str
    source_column_id: str
    target_sheet_id: str
    target_column_id: str
    source_observed_count: int
    source_non_missing_count: int
    source_distinct_count: int
    target_observed_count: int
    target_non_missing_count: int
    target_distinct_count: int
    source_complete: bool
    source_unique: bool
    target_complete: bool
    target_unique: bool
    referential_coverage_ratio: float
    uncovered_reference_distinct_count: int
    source_or_target_sensitive: bool
    source_or_target_has_formula: bool


def _signature(value: object) -> tuple[str, str] | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        return ("text", unicodedata.normalize("NFKC", value)) if not value.startswith("=") else None
    if isinstance(value, int):
        return ("integer", str(value))
    if isinstance(value, float):
        return ("float", repr(value)) if math.isfinite(value) else None
    if isinstance(value, datetime):
        return ("datetime", value.isoformat())
    if isinstance(value, date):
        return ("date", value.isoformat())
    return None


@dataclass
class RelationshipColumnAccumulator:
    """Acumulador descartável de uma coluna elegível, sem armazenar o cabeçalho."""

    sensitive_header: bool = False
    observed_count: int = 0
    non_missing_count: int = 0
    has_formula: bool = False
    _signatures: set[tuple[str, str]] = field(default_factory=set, repr=False)

    def consume(self, value: object, *, is_formula: bool) -> None:
        self.observed_count += 1
        self.has_formula = self.has_formula or is_formula
        if missing_class(value) is not None or is_formula:
            return
        self.non_missing_count += 1
        signature = _signature(value)
        if signature is not None:
            self._signatures.add(signature)

    @property
    def distinct_count(self) -> int:
        return len(self._signatures)

    @property
    def complete(self) -> bool:
        return self.observed_count > 0 and self.non_missing_count == self.observed_count

    @property
    def unique(self) -> bool:
        return self.complete and self.distinct_count == self.non_missing_count

    def coverage_from(self, reference: "RelationshipColumnAccumulator") -> float:
        if not self._signatures:
            return 0.0
        return round(len(self._signatures.intersection(reference._signatures)) / len(self._signatures), 8)

    def uncovered_distinct_count_from(self, reference: "RelationshipColumnAccumulator") -> int:
        """Retorna somente a contagem agregada de assinaturas sem cobertura."""

        return len(self._signatures.difference(reference._signatures))

    def clear(self) -> None:
        self._signatures.clear()
