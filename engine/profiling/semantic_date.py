"""Perfil agregado e privado para reconhecimento estrito de datas semânticas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from engine.profiling.bad_dates import BR_DATE_HYPHEN_TEXT, BR_DATE_SLASH_TEXT, ISO_DATE_TEXT


SEMANTIC_DATE_BASIS = "physical_date_or_strict_iso_br_hyphen_br_slash_100pct_min10_v1"


@dataclass(frozen=True)
class SemanticDateProfile:
    non_missing_count: int = 0
    physical_date_count: int = 0
    iso_text_count: int = 0
    br_hyphen_text_count: int = 0
    br_slash_text_count: int = 0
    recognized_date_count: int = 0
    recognized_date_ratio: float = 0.0
    basis: str = SEMANTIC_DATE_BASIS


def _valid_text_date(value: str) -> str | None:
    if ISO_DATE_TEXT.fullmatch(value):
        fmt, kind = "%Y-%m-%d", "iso"
    elif BR_DATE_HYPHEN_TEXT.fullmatch(value):
        fmt, kind = "%d-%m-%Y", "br_hyphen"
    elif BR_DATE_SLASH_TEXT.fullmatch(value):
        fmt, kind = "%d/%m/%Y", "br_slash"
    else:
        return None
    try:
        datetime.strptime(value, fmt)
    except ValueError:
        return None
    return kind


def profile_semantic_date(values: list[object]) -> SemanticDateProfile:
    """Reconhece apenas datas físicas e três gramáticas textuais válidas, sem reter valores."""
    non_missing = physical = iso = hyphen = slash = recognized = 0
    for value in values:
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        non_missing += 1
        if isinstance(value, (date, datetime)) and not isinstance(value, bool):
            physical += 1
            recognized += 1
            continue
        if isinstance(value, str):
            kind = _valid_text_date(value.strip())
            if kind:
                recognized += 1
                if kind == "iso":
                    iso += 1
                elif kind == "br_hyphen":
                    hyphen += 1
                else:
                    slash += 1
    return SemanticDateProfile(
        non_missing_count=non_missing, physical_date_count=physical, iso_text_count=iso,
        br_hyphen_text_count=hyphen, br_slash_text_count=slash, recognized_date_count=recognized,
        recognized_date_ratio=(recognized / non_missing if non_missing else 0.0),
    )
