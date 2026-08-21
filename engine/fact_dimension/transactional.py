"""MDL-FACTTXN-002: hipótese conservadora de fato transacional."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.transactional_fact import TransactionalDateProfile


@dataclass(frozen=True)
class TransactionalFactSheetProfile:
    observed_row_count: int
    grain_available: bool
    transactional_dates: tuple[TransactionalDateProfile, ...]
    eligible_measure_column_count: int


def classify_transactional_fact(profile: TransactionalFactSheetProfile) -> list[dict[str, object]]:
    temporal_columns = tuple(
        item for item in profile.transactional_dates
        if item.recognized_date_count > 0
        and item.distinct_date_count / item.recognized_date_count >= 0.80
    )
    if (
        not profile.grain_available
        or profile.observed_row_count < 20
        or not temporal_columns
        or profile.eligible_measure_column_count < 1
    ):
        return []
    return [{
        "rule_id": "MDL-FACTTXN-002",
        "classification_type": "fact_transactional_candidate",
        "confidence": 0.70,
        "evidence": {
            "observed_row_count": profile.observed_row_count,
            "eligible_temporal_column_count": len(temporal_columns),
            "distinct_date_count": max(item.distinct_date_count for item in temporal_columns),
            "temporal_distinct_ratio": max(
                item.distinct_date_count / item.recognized_date_count for item in temporal_columns
            ),
            "eligible_measure_column_count": profile.eligible_measure_column_count,
            "grain_available": True,
            "basis": "grain_temporal_distinct_ratio_gte_080_measure_min20_private_v1",
        },
        "question": {
            "text": "Confirme se cada linha representa um evento ou lançamento individual no tempo.",
            "reason": "Granularidade, alta variabilidade temporal e medidas sugerem transações, mas a semântica de negócio exige validação humana.",
            "question_type": "confirmation", "priority": "high", "blocking": True, "options": [],
        },
    }]
