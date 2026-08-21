"""Perfil privado para a classificação semântica conservadora de quantidade."""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_quantity_headers_with_finite_physical_numbers"
AUTHORIZED_HEADERS = frozenset({"quantidade", "qtd", "qtde"})


@dataclass(frozen=True)
class SemanticQuantityProfile:
    header_eligible: bool = False
    physical_numeric_count: int = 0
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


def profile_semantic_quantity(header: object, values: Iterable[object]) -> SemanticQuantityProfile:
    """Retém somente a elegibilidade fechada do cabeçalho e a contagem física agregada."""

    physical_numeric_count = sum(1 for value in values if _is_physical_finite_number(value))
    return SemanticQuantityProfile(
        header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS,
        physical_numeric_count=physical_numeric_count,
    )
