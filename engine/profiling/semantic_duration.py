"""Perfil privado e agregado para a SEM-DUR-008."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
import re
import unicodedata
from typing import Iterable


_DURATION_HEADERS = frozenset({
    "duracao",
    "duracao (horas)",
    "duracao (minutos)",
    "duracao (segundos)",
    "duracao (dias)",
})


@dataclass(frozen=True)
class SemanticDurationProfile:
    """Sinais irreversíveis; nunca preserva valores nem cabeçalhos."""

    header_eligible: bool = False
    non_missing_count: int = 0
    physical_finite_numeric_count: int = 0
    ambiguity_count: int = 0
    basis: str = "closed_duration_headers_with_aggregate_physical_numeric_signals"


def _normalize_header(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).casefold()
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", normalized.strip())


def _is_missing(value: object) -> bool:
    return value is None or (isinstance(value, float) and value != value) or (isinstance(value, str) and not value.strip())


def _is_physical_finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(float(value))


def profile_semantic_duration(header: str, values: Iterable[object]) -> SemanticDurationProfile:
    """Deriva apenas booleanos e contagens agregadas durante o profiling transitório."""

    materialized = tuple(values)
    non_missing_count = sum(1 for value in materialized if not _is_missing(value))
    physical_finite_numeric_count = sum(1 for value in materialized if _is_physical_finite_number(value))
    return SemanticDurationProfile(
        header_eligible=_normalize_header(header) in _DURATION_HEADERS,
        non_missing_count=non_missing_count,
        physical_finite_numeric_count=physical_finite_numeric_count,
        ambiguity_count=non_missing_count - physical_finite_numeric_count,
    )
