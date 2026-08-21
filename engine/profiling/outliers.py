"""Perfil agregado de extremos estatísticos pela política Tukey autorizada."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable


OUTLIER_BASIS = "tukey_iqr_1_5_linear_quantile_finite_physical_numeric_80pct_min20_v1"
MINIMUM_PHYSICAL_NUMERIC_COUNT = 20
MINIMUM_NUMERIC_SHARE = 0.8


@dataclass(frozen=True)
class OutlierProfile:
    eligible: bool = False
    physical_nonempty_count: int = 0
    physical_numeric_count: int = 0
    lower_outlier_count: int = 0
    upper_outlier_count: int = 0
    outlier_count: int = 0
    outlier_ratio: float = 0.0
    basis: str = OUTLIER_BASIS


def _is_physical_nonempty(value: object) -> bool:
    return value is not None and not (isinstance(value, str) and not value.strip())


def _is_physical_finite_number(value: object) -> bool:
    if isinstance(value, bool) or isinstance(value, (date, datetime)):
        return False
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def _linear_quantile(sorted_values: list[float], probability: float) -> float:
    position = probability * (len(sorted_values) - 1)
    lower_index = math.floor(position)
    upper_index = math.ceil(position)
    if lower_index == upper_index:
        return sorted_values[lower_index]
    lower_value = sorted_values[lower_index]
    upper_value = sorted_values[upper_index]
    return lower_value + (upper_value - lower_value) * (position - lower_index)


def profile_outliers(values: Iterable[object]) -> OutlierProfile:
    """Calcula candidatos transitoriamente e retorna somente métricas agregadas privadas."""

    physical_nonempty_count = 0
    numeric_values: list[float] = []
    for value in values:
        if not _is_physical_nonempty(value):
            continue
        physical_nonempty_count += 1
        if _is_physical_finite_number(value):
            numeric_values.append(float(value))

    physical_numeric_count = len(numeric_values)
    numeric_share = physical_numeric_count / physical_nonempty_count if physical_nonempty_count else 0.0
    if physical_numeric_count < MINIMUM_PHYSICAL_NUMERIC_COUNT or numeric_share < MINIMUM_NUMERIC_SHARE:
        return OutlierProfile(
            physical_nonempty_count=physical_nonempty_count,
            physical_numeric_count=physical_numeric_count,
        )

    numeric_values.sort()
    lower_quartile = _linear_quantile(numeric_values, 0.25)
    upper_quartile = _linear_quantile(numeric_values, 0.75)
    interquartile_range = upper_quartile - lower_quartile
    if interquartile_range == 0:
        return OutlierProfile(
            physical_nonempty_count=physical_nonempty_count,
            physical_numeric_count=physical_numeric_count,
        )

    lower_fence = lower_quartile - 1.5 * interquartile_range
    upper_fence = upper_quartile + 1.5 * interquartile_range
    lower_outlier_count = sum(value < lower_fence for value in numeric_values)
    upper_outlier_count = sum(value > upper_fence for value in numeric_values)
    outlier_count = lower_outlier_count + upper_outlier_count
    return OutlierProfile(
        eligible=True,
        physical_nonempty_count=physical_nonempty_count,
        physical_numeric_count=physical_numeric_count,
        lower_outlier_count=lower_outlier_count,
        upper_outlier_count=upper_outlier_count,
        outlier_count=outlier_count,
        outlier_ratio=round(outlier_count / physical_numeric_count, 8),
    )
