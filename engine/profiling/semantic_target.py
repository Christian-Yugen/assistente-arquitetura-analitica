"""Perfil privado para a classificação semântica conservadora de meta ou previsto."""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_target_headers_with_finite_physical_numbers"
AUTHORIZED_HEADERS = frozenset({
    "meta",
    "previsto",
    "previsao",
    "orcado",
    "orcamento",
    "forecast",
    "target",
    "budget",
    "planejado",
})


@dataclass(frozen=True)
class SemanticTargetProfile:
    header_eligible: bool = False
    physical_numeric_count: int = 0
    zero_value_count: int = 0
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


def profile_semantic_target(header: object, values: Iterable[object]) -> SemanticTargetProfile:
    """Retém somente a elegibilidade fechada do cabeçalho e a contagem física agregada."""

    materialized_values = tuple(values)
    physical_numeric_count = sum(1 for value in materialized_values if _is_physical_finite_number(value))
    zero_value_count = sum(1 for value in materialized_values if _is_physical_finite_number(value) and float(value) == 0.0)
    return SemanticTargetProfile(
        header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS,
        physical_numeric_count=physical_numeric_count,
        zero_value_count=zero_value_count,
    )
