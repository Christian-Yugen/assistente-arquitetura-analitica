"""Profiling determinístico para a QLT-NUMTEXT-007 sem manter valores brutos."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Literal

from engine.quality.numtext import CANONICAL_NUMERIC_TEXT_BASIS


STRICT_CANONICAL_NUMBER = re.compile(r"^[+-]?(?:0|[1-9]\d*)(?:\.\d+)?$")
LOCALE_AMBIGUOUS_NUMBER = re.compile(r"^[+-]?\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?$")
PhysicalType = Literal["text", "mixed", "numeric", "date", "boolean", "unknown"]


@dataclass(frozen=True)
class NumericTextProfile:
    non_empty_value_count: int
    numeric_text_candidate_count: int
    numeric_text_candidate_ratio: float
    numeric_text_basis: str
    numeric_text_ambiguity_count: int


def infer_physical_type(values: Iterable[object]) -> PhysicalType:
    non_empty = [value for value in values if value is not None and str(value).strip() != ""]
    if not non_empty:
        return "unknown"
    if all(isinstance(value, bool) for value in non_empty):
        return "boolean"
    if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in non_empty):
        return "numeric"
    if all(isinstance(value, str) for value in non_empty):
        return "text"
    return "mixed"


def profile_numeric_text(values: Iterable[object]) -> NumericTextProfile:
    """Conta somente atributos agregados que o executor pode repassar ao contrato."""

    non_empty_values = [value for value in values if value is not None and str(value).strip() != ""]
    text_values = [value.strip() for value in non_empty_values if isinstance(value, str)]
    candidates = [value for value in text_values if STRICT_CANONICAL_NUMBER.fullmatch(value)]
    ambiguous = [
        value
        for value in text_values
        if not STRICT_CANONICAL_NUMBER.fullmatch(value) and LOCALE_AMBIGUOUS_NUMBER.fullmatch(value)
    ]
    non_empty_count = len(non_empty_values)

    return NumericTextProfile(
        non_empty_value_count=non_empty_count,
        numeric_text_candidate_count=len(candidates),
        numeric_text_candidate_ratio=round(len(candidates) / non_empty_count, 8) if non_empty_count else 0.0,
        numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
        numeric_text_ambiguity_count=len(ambiguous),
    )
