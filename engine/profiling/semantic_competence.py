"""Perfil privado e agregado para a hipótese de data de competência."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


NORMALIZATION_BASIS = "nfkc_casefold_accentless_collapsed_ptbr_closed_competence_headers_v1"
AUTHORIZED_HEADERS = frozenset({"competencia", "data competencia", "data de competencia"})


@dataclass(frozen=True)
class SemanticCompetenceProfile:
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


def profile_semantic_competence(header: object) -> SemanticCompetenceProfile:
    """Deriva somente a elegibilidade transitória de cabeçalho fechado."""

    return SemanticCompetenceProfile(header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS)
