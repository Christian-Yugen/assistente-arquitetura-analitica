"""Perfil agregado para valores negativos em medidas explicitamente elegíveis."""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_nonnegative_measure_headers_with_finite_physical_numbers"
AUTHORIZED_HEADERS = frozenset({"quantidade", "qtd", "estoque", "volume", "idade"})


@dataclass(frozen=True)
class NegativeValuesProfile:
    header_eligible: bool = False
    physical_numeric_count: int = 0
    negative_physical_count: int = 0
    negative_physical_ratio: float = 0.0
    basis: str = NORMALIZATION_BASIS


def _normalize_header(header: object) -> str | None:
    if not isinstance(header, str):
        return None
    normalized = unicodedata.normalize("NFKC", header).casefold().strip()
    accentless = "".join(
        character
        for character in unicodedata.normalize("NFKD", normalized)
        if not unicodedata.combining(character)
    )
    return re.sub(r"\s+", " ", accentless)


def _is_physical_finite_number(value: object) -> bool:
    if isinstance(value, bool) or isinstance(value, (date, datetime)):
        return False
    if not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


@dataclass
class NegativeValuesAccumulator:
    """Conta somente números físicos finitos, sem persistir cabeçalho, valor ou posição."""

    header_eligible: bool
    physical_numeric_count: int = 0
    negative_physical_count: int = 0

    def consume(self, value: object) -> None:
        if not _is_physical_finite_number(value):
            return
        self.physical_numeric_count += 1
        if value < 0:  # type: ignore[operator]
            self.negative_physical_count += 1

    def finalize(self) -> NegativeValuesProfile:
        ratio = self.negative_physical_count / self.physical_numeric_count if self.physical_numeric_count else 0.0
        return NegativeValuesProfile(
            header_eligible=self.header_eligible,
            physical_numeric_count=self.physical_numeric_count,
            negative_physical_count=self.negative_physical_count,
            negative_physical_ratio=round(ratio, 8),
        )


def profile_negative_values(header: object, values: Iterable[object]) -> NegativeValuesProfile:
    """Produz perfil privado para a política autorizada sem transportar dados de célula."""

    accumulator = NegativeValuesAccumulator(header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS)
    for value in values:
        accumulator.consume(value)
    return accumulator.finalize()
