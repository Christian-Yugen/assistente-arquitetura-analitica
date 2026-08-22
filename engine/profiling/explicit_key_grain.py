"""Perfil privado para a GRN-EXPL-002 sem retenção de cabeçalhos ou valores."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata


NORMALIZATION_BASIS = "nfkc_casefold_strip_accents_collapse_spaces_v1"
AUTHORIZED_HEADERS = frozenset({"id", "chave", "key"})


def _normalize_header(header: object) -> str:
    value = unicodedata.normalize("NFKC", str(header)).casefold().strip()
    value = "".join(
        character for character in unicodedata.normalize("NFD", value)
        if unicodedata.category(character) != "Mn"
    )
    return re.sub(r"\s+", " ", value)


@dataclass(frozen=True)
class ExplicitKeyHeaderProfile:
    """Sinal transitório de cabeçalho, reduzido a booleano e base técnica."""

    header_eligible: bool = False
    basis: str = NORMALIZATION_BASIS


def profile_explicit_key_header(header: object) -> ExplicitKeyHeaderProfile:
    """Deriva somente a elegibilidade, descartando o cabeçalho normalizado."""

    return ExplicitKeyHeaderProfile(header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS)
