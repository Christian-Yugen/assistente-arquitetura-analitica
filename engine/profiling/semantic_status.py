"""Perfil privado e agregado para a hipótese de status."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable

from engine.profiling.missingness import missing_class


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_status_headers_v1"
AUTHORIZED_HEADERS = frozenset({"status", "situacao", "estado"})


@dataclass(frozen=True)
class SemanticStatusProfile:
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


def profile_semantic_status(header: object, values: Iterable[object]) -> SemanticStatusProfile:
    """Descarta o conteúdo após derivar apenas contagens de tipo físico e ambiguidade."""

    physical_text_count = 0
    ambiguity_count = 0
    for value in values:
        if missing_class(value) is not None:
            continue
        if isinstance(value, str) and value.strip() and not value.startswith("="):
            physical_text_count += 1
        else:
            ambiguity_count += 1
    return SemanticStatusProfile(
        header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS,
        physical_text_count=physical_text_count,
        ambiguity_count=ambiguity_count,
    )
