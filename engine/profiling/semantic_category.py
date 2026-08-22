"""Perfil privado e agregado para a hipótese de categoria."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable

from engine.profiling.missingness import missing_class


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_category_header_v1"
AUTHORIZED_HEADERS = frozenset({"categoria"})


@dataclass(frozen=True)
class SemanticCategoryProfile:
    header_eligible: bool = False
    physical_text_count: int = 0
    ambiguity_count: int = 0
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


def profile_semantic_category(header: object, values: Iterable[object]) -> SemanticCategoryProfile:
    """Descarta o conteúdo após derivar somente sinais agregados autorizados."""

    physical_text_count = 0
    ambiguity_count = 0
    for value in values:
        if missing_class(value) is not None:
            continue
        if isinstance(value, str) and value.strip() and not value.startswith("="):
            physical_text_count += 1
        else:
            ambiguity_count += 1
    return SemanticCategoryProfile(
        header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS,
        physical_text_count=physical_text_count,
        ambiguity_count=ambiguity_count,
    )
