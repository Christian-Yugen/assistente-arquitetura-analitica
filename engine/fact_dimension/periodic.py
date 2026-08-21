"""MDL-FACTPER-001: hipótese conservadora de fato periódica."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.periodic_fact import PeriodicDateProfile


@dataclass(frozen=True)
class PeriodicFactSheetProfile:
    observed_row_count: int
    grain_available: bool
    periodic_dates: tuple[PeriodicDateProfile, ...]
    eligible_measure_column_count: int


def classify_periodic_fact(profile: PeriodicFactSheetProfile) -> list[dict[str, object]]:
    temporal_columns = tuple(item for item in profile.periodic_dates if item.distinct_period_count >= 2)
    if (
        not profile.grain_available
        or profile.observed_row_count < 20
        or not temporal_columns
        or profile.eligible_measure_column_count < 1
    ):
        return []
    return [{
        "rule_id": "MDL-FACTPER-001",
        "classification_type": "fact_periodic_candidate",
        "confidence": 0.70,
        "evidence": {
            "observed_row_count": profile.observed_row_count,
            "eligible_temporal_column_count": len(temporal_columns),
            "distinct_period_count": max(item.distinct_period_count for item in temporal_columns),
            "eligible_measure_column_count": profile.eligible_measure_column_count,
            "grain_available": True,
            "basis": "grain_temporal_measure_min20_private_v1",
        },
        "question": {
            "text": "Confirme se cada linha representa o estado ou uma medida de uma entidade em um período de referência.",
            "reason": "A presença de granularidade, períodos e medidas é uma hipótese técnica; a semântica de negócio exige validação humana.",
            "question_type": "confirmation", "priority": "high", "blocking": True, "options": [],
        },
    }]
