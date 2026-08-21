"""Profiling privado de ausência e duplicidade exata para identificadores elegíveis."""

from __future__ import annotations

import math
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable

from engine.profiling.missingness import missing_class


NORMALIZATION_BASIS = "header_nfkc_casefold_ascii_space__value_type_tagged_nfkc_exact_v1"
ELIGIBLE_HEADERS = frozenset({"id", "codigo", "cod", "chave", "matricula", "cpf", "cnpj", "numero", "num"})


@dataclass(frozen=True)
class IdentifierCompletenessProfile:
    header_eligible: bool = False
    observed_cell_count: int = 0
    missing_cell_count: int = 0
    non_missing_cell_count: int = 0
    duplicate_group_count: int = 0
    duplicate_occurrence_count: int = 0
    missing_ratio: float = 0.0
    duplicate_ratio: float = 0.0
    basis: str = NORMALIZATION_BASIS


def _normalize_header(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", unicodedata.normalize("NFKC", value))
    without_accents = "".join(character for character in decomposed if not unicodedata.combining(character))
    return " ".join(without_accents.casefold().strip().split())


def _value_signature(value: object) -> tuple[str, str] | None:
    """Cria assinatura exata tipada apenas durante a contagem; nunca a expõe no perfil."""

    if isinstance(value, bool):
        return ("boolean", str(value).lower())
    if isinstance(value, str):
        if value.startswith("="):
            return None
        return ("text", unicodedata.normalize("NFKC", value))
    if isinstance(value, int):
        return ("integer", str(value))
    if isinstance(value, float):
        if not math.isfinite(value):
            return None
        return ("float", repr(value))
    if isinstance(value, datetime):
        return ("datetime", value.isoformat())
    if isinstance(value, date):
        return ("date", value.isoformat())
    return None


class IdentifierCompletenessAccumulator:
    """Descarta cabeçalho e assinaturas de valores ao finalizar a coluna."""

    def __init__(self, header: str) -> None:
        self._header_eligible = _normalize_header(header) in ELIGIBLE_HEADERS
        self._observed_cell_count = 0
        self._missing_cell_count = 0
        self._non_missing_cell_count = 0
        self._counts: Counter[tuple[str, str]] = Counter()

    def consume(self, value: object) -> None:
        self._observed_cell_count += 1
        if missing_class(value) is not None:
            self._missing_cell_count += 1
            return
        self._non_missing_cell_count += 1
        signature = _value_signature(value)
        if signature is not None:
            self._counts[signature] += 1

    def finalize(self) -> IdentifierCompletenessProfile:
        duplicate_sizes = [count for count in self._counts.values() if count >= 2]
        duplicate_occurrence_count = sum(duplicate_sizes)
        result = IdentifierCompletenessProfile(
            header_eligible=self._header_eligible,
            observed_cell_count=self._observed_cell_count,
            missing_cell_count=self._missing_cell_count,
            non_missing_cell_count=self._non_missing_cell_count,
            duplicate_group_count=len(duplicate_sizes),
            duplicate_occurrence_count=duplicate_occurrence_count,
            missing_ratio=round(self._missing_cell_count / self._observed_cell_count, 8) if self._observed_cell_count else 0.0,
            duplicate_ratio=round(duplicate_occurrence_count / self._observed_cell_count, 8) if self._observed_cell_count else 0.0,
        )
        self._counts.clear()
        return result


def profile_identifier_completeness(header: str, values: Iterable[object]) -> IdentifierCompletenessProfile:
    accumulator = IdentifierCompletenessAccumulator(header)
    for value in values:
        accumulator.consume(value)
    return accumulator.finalize()
