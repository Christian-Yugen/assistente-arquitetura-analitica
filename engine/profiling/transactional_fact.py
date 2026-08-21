"""Métricas privadas de variabilidade temporal para hipótese de fato transacional."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from engine.profiling.periodic_fact import _period_bucket


TRANSACTIONAL_FACT_DATE_BASIS = "strict_semantic_date_distinct_days_private_v1"


@dataclass(frozen=True)
class TransactionalDateProfile:
    recognized_date_count: int = 0
    distinct_date_count: int = 0
    basis: str = TRANSACTIONAL_FACT_DATE_BASIS


def _date_bucket(value: object) -> tuple[int, int, int] | None:
    if isinstance(value, (date, datetime)) and not isinstance(value, bool):
        return value.year, value.month, value.day
    period = _period_bucket(value)
    if period is None or not isinstance(value, str):
        return None
    text = value.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.year, parsed.month, parsed.day
        except ValueError:
            continue
    return None


def profile_transactional_date(values: list[object]) -> TransactionalDateProfile:
    """Conta dias distintos sem reter valores, datas ou buckets."""
    buckets: set[tuple[int, int, int]] = set()
    recognized = 0
    for value in values:
        bucket = _date_bucket(value)
        if bucket is not None:
            recognized += 1
            buckets.add(bucket)
    return TransactionalDateProfile(recognized_date_count=recognized, distinct_date_count=len(buckets))
