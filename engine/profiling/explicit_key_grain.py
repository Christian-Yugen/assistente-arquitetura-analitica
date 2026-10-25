"""Perfil privado para a GRN-EXPL-002 sem retenção de cabeçalhos ou valores."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata


NORMALIZATION_BASIS = "nfkc_casefold_strip_accents_collapse_spaces_v1"
AUTHORIZED_HEADERS = frozenset({"id", "chave", "key"})
COMPOUND_IDENTIFIER_TOKENS = frozenset({"codigo", "cod", "matricula", "numero", "num"})


def _normalize_header(header: object) -> str:
    value = unicodedata.normalize("NFKC", str(header)).casefold().strip()
    value = "".join(
        character for character in unicodedata.normalize("NFD", value)
        if unicodedata.category(character) != "Mn"
    )
    return re.sub(r"\s+", " ", value)


def _header_tokens(header: object) -> frozenset[str]:
    normalized = _normalize_header(header).replace("_", " ")
    return frozenset(re.findall(r"[a-z0-9]+", normalized))


@dataclass(frozen=True)
class ExplicitKeyHeaderProfile:
    """Sinal transitório de cabeçalho, reduzido a booleano e base técnica."""

    header_eligible: bool = False
    basis: str = NORMALIZATION_BASIS


def profile_explicit_key_header(header: object) -> ExplicitKeyHeaderProfile:
    """Deriva somente a elegibilidade, descartando o cabeçalho normalizado."""

    normalized = _normalize_header(header)
    tokens = _header_tokens(header)
    return ExplicitKeyHeaderProfile(
        header_eligible=(
            normalized in AUTHORIZED_HEADERS
            or (len(tokens) > 1 and bool(tokens.intersection(COMPOUND_IDENTIFIER_TOKENS)))
        )
    )
