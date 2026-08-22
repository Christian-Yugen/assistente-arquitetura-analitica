"""Perfil privado da GRN-EVENT-004 sem retenção de cabeçalhos ou valores."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata


NORMALIZATION_BASIS = "nfkc_casefold_strip_accents_collapse_spaces_v1"
AUTHORIZED_HEADERS = frozenset({"evento", "transacao", "ocorrencia"})


def _normalize_header(header: object) -> str:
    value = unicodedata.normalize("NFKC", str(header)).casefold().strip()
    value = "".join(
        character for character in unicodedata.normalize("NFD", value)
        if unicodedata.category(character) != "Mn"
    )
    return re.sub(r"\s+", " ", value)


@dataclass(frozen=True)
class EventMarkerHeaderProfile:
    """Sinal transitório de marcador de evento reduzido a um booleano."""

    header_eligible: bool = False
    basis: str = NORMALIZATION_BASIS


def profile_event_marker_header(header: object) -> EventMarkerHeaderProfile:
    """Deriva elegibilidade de vocabulário fechado e descarta a entrada normalizada."""

    return EventMarkerHeaderProfile(header_eligible=_normalize_header(header) in AUTHORIZED_HEADERS)
