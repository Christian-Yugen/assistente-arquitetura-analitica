"""Perfil privado e agregado para a hipótese de nome ou descrição."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_description_headers_v1"
AUTHORIZED_HEADERS = frozenset({"nome", "descricao"})


@dataclass(frozen=True)
class SemanticDescriptionProfile:
    header_eligible: bool = False
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


def profile_semantic_description(header: object) -> SemanticDescriptionProfile:
    """Deriva apenas a elegibilidade transitória de um cabeçalho fechado."""

    return SemanticDescriptionProfile(header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS)
