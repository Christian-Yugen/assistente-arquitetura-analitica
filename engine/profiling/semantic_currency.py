"""Perfil privado para a classificação semântica conservadora de valor monetário."""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_currency_headers_with_explicit_excel_currency_format"
AUTHORIZED_HEADERS = frozenset({
    "preco",
    "preco unitario",
    "preco total",
    "valor monetario",
    "valor financeiro",
    "valor total",
    "receita",
    "faturamento",
    "custo",
    "custo total",
    "despesa",
    "saldo",
})
_CURRENCY_MARKERS = frozenset({"R$", "$", "€", "£", "¥", "₹", "¤"})


@dataclass(frozen=True)
class SemanticCurrencyProfile:
    header_eligible: bool = False
    physical_numeric_count: int = 0
    currency_format_numeric_count: int = 0
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
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def has_explicit_currency_format(number_format: object) -> bool:
    """Reconhece somente marcadores monetários explícitos sem reter o formato."""

    return isinstance(number_format, str) and any(marker in number_format for marker in _CURRENCY_MARKERS)


@dataclass
class SemanticCurrencyAccumulator:
    """Reduz metadados transitórios de células a contagens privadas por coluna."""

    header: object
    physical_numeric_count: int = 0
    currency_format_numeric_count: int = 0

    def consume(self, value: object, *, has_currency_format: bool) -> None:
        if not _is_physical_finite_number(value):
            return
        self.physical_numeric_count += 1
        if has_currency_format:
            self.currency_format_numeric_count += 1

    def finalize(self) -> SemanticCurrencyProfile:
        return SemanticCurrencyProfile(
            header_eligible=_normalize_header(self.header) in AUTHORIZED_HEADERS,
            physical_numeric_count=self.physical_numeric_count,
            currency_format_numeric_count=self.currency_format_numeric_count,
        )


def profile_semantic_currency(
    header: object,
    values: Iterable[object],
    number_formats: Iterable[object] | None = None,
) -> SemanticCurrencyProfile:
    """Retém somente elegibilidade fechada e contagens agregadas de formato monetário."""

    accumulator = SemanticCurrencyAccumulator(header=header)
    formats = number_formats if number_formats is not None else ()
    if number_formats is None:
        for value in values:
            accumulator.consume(value, has_currency_format=False)
    else:
        for value, number_format in zip(values, formats, strict=True):
            accumulator.consume(value, has_currency_format=has_explicit_currency_format(number_format))
    return accumulator.finalize()
