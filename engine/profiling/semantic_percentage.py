"""Perfil privado para a classificação semântica conservadora de percentual."""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_percentage_headers_with_unit_interval_finite_physical_numbers"
AUTHORIZED_HEADERS = frozenset({"percentual", "percentagem", "pct", "%"})


@dataclass(frozen=True)
class SemanticPercentageProfile:
    header_eligible: bool = False
    physical_numeric_count: int = 0
    in_range_numeric_count: int = 0
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


def profile_semantic_percentage(header: object, values: Iterable[object]) -> SemanticPercentageProfile:
    """Retém apenas elegibilidade fechada e contagens agregadas de proporções físicas."""

    physical_numeric_count = 0
    in_range_numeric_count = 0
    for value in values:
        if not _is_physical_finite_number(value):
            continue
        physical_numeric_count += 1
        if 0.0 <= float(value) <= 1.0:
            in_range_numeric_count += 1
    return SemanticPercentageProfile(
        header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS,
        physical_numeric_count=physical_numeric_count,
        in_range_numeric_count=in_range_numeric_count,
    )
