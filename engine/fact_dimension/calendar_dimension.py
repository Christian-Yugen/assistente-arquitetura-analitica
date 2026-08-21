"""MDL-DIMCAL-006: hipótese conservadora de dimensão calendário."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.calendar_dimension import CalendarDateProfile


@dataclass(frozen=True)
class CalendarDimensionSheetProfile:
    observed_row_count: int
    grain_available: bool
    calendar_dates: tuple[CalendarDateProfile, ...]
    eligible_measure_column_count: int


def classify_calendar_dimension(profile: CalendarDimensionSheetProfile) -> list[dict[str, object]]:
    eligible_dates = tuple(
        item
        for item in profile.calendar_dates
        if item.recognized_date_count == profile.observed_row_count
        and item.distinct_date_count == item.recognized_date_count
        and item.consecutive_day_transition_count == item.distinct_date_count - 1
    )
    if (
        not profile.grain_available
        or profile.observed_row_count < 20
        or not eligible_dates
        or profile.eligible_measure_column_count > 0
    ):
        return []
    strongest = max(eligible_dates, key=lambda item: item.distinct_date_count)
    return [{
        "rule_id": "MDL-DIMCAL-006",
        "classification_type": "dimension_calendar_candidate",
        "confidence": 0.75,
        "evidence": {
            "observed_row_count": profile.observed_row_count,
            "eligible_calendar_column_count": len(eligible_dates),
            "recognized_date_count": strongest.recognized_date_count,
            "distinct_date_count": strongest.distinct_date_count,
            "consecutive_day_transition_count": strongest.consecutive_day_transition_count,
            "eligible_measure_column_count": profile.eligible_measure_column_count,
            "grain_available": True,
            "basis": "grain_unique_daily_dates_no_measure_min20_private_v1",
        },
        "question": {
            "text": "Confirme se esta aba representa um calendário de referência, com uma linha por dia, usado para analisar outras tabelas.",
            "reason": "Datas físicas únicas e consecutivas, sem medidas, sugerem dimensão calendário, mas a finalidade de negócio exige validação humana.",
            "question_type": "confirmation", "priority": "high", "blocking": True, "options": [],
        },
    }]
