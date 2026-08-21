"""Métricas temporais privadas para a hipótese de dimensão calendário por aba."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from engine.profiling.bad_dates import BR_DATE_HYPHEN_TEXT, BR_DATE_SLASH_TEXT, ISO_DATE_TEXT


CALENDAR_DIMENSION_DATE_BASIS = "strict_semantic_date_daily_continuity_private_v1"


@dataclass(frozen=True)
class CalendarDateProfile:
    recognized_date_count: int = 0
    distinct_date_count: int = 0
    consecutive_day_transition_count: int = 0
    basis: str = CALENDAR_DIMENSION_DATE_BASIS


def _parse_strict_date(value: object) -> date | None:
    if isinstance(value, datetime) and not isinstance(value, bool):
        return value.date()
    if isinstance(value, date) and not isinstance(value, bool):
        return value
    if not isinstance(value, str):
        return None
    text = value.strip()
    if ISO_DATE_TEXT.fullmatch(text):
        fmt = "%Y-%m-%d"
    elif BR_DATE_HYPHEN_TEXT.fullmatch(text):
        fmt = "%d-%m-%Y"
    elif BR_DATE_SLASH_TEXT.fullmatch(text):
        fmt = "%d/%m/%Y"
    else:
        return None
    try:
        return datetime.strptime(text, fmt).date()
    except ValueError:
        return None


def profile_calendar_date(values: list[object]) -> CalendarDateProfile:
    """Conta datas e continuidade diária sem reter os valores temporais observados."""
    recognized_dates = [parsed for value in values if (parsed := _parse_strict_date(value)) is not None]
    distinct_dates = sorted(set(recognized_dates))
    consecutive_transitions = sum(
        1
        for current, following in zip(distinct_dates, distinct_dates[1:])
        if (following - current).days == 1
    )
    return CalendarDateProfile(
        recognized_date_count=len(recognized_dates),
        distinct_date_count=len(distinct_dates),
        consecutive_day_transition_count=consecutive_transitions,
    )
