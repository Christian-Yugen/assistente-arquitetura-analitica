"""Métricas privadas para a hipótese de fato periódica por aba."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from engine.profiling.bad_dates import BR_DATE_HYPHEN_TEXT, BR_DATE_SLASH_TEXT, ISO_DATE_TEXT


PERIODIC_FACT_DATE_BASIS = "strict_semantic_date_distinct_months_private_v1"


@dataclass(frozen=True)
class PeriodicDateProfile:
    recognized_date_count: int = 0
    distinct_period_count: int = 0
    basis: str = PERIODIC_FACT_DATE_BASIS


def _period_bucket(value: object) -> tuple[int, int] | None:
    if isinstance(value, (date, datetime)) and not isinstance(value, bool):
        return value.year, value.month
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
        parsed = datetime.strptime(text, fmt)
    except ValueError:
        return None
    return parsed.year, parsed.month


def profile_periodic_date(values: list[object]) -> PeriodicDateProfile:
    """Conta meses distintos sem reter datas, buckets ou valores brutos."""
    buckets: set[tuple[int, int]] = set()
    recognized = 0
    for value in values:
        bucket = _period_bucket(value)
        if bucket is not None:
            recognized += 1
            buckets.add(bucket)
    return PeriodicDateProfile(recognized_date_count=recognized, distinct_period_count=len(buckets))
