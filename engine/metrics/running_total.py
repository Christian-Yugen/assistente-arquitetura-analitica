"""MET-RUNNING-010: recomendação conceitual privada para acumulado."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunningTotalConceptProfile:
    row_count: int = 0
    physical_column_count: int = 0
    measure_candidate_count: int = 0
    temporal_order_candidate_count: int = 0
    temporal_order_duplicate_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_running_total_concept(profile: RunningTotalConceptProfile) -> dict[str, object] | None:
    blocked = (
        profile.has_sensitive_signal
        or profile.has_formula_signal
        or profile.has_undefined_classification
        or profile.has_fact_without_grain
        or profile.classification_conflict_count > 0
        or profile.grain_ambiguity_count > 0
        or profile.temporal_order_duplicate_count > 0
    )
    if blocked or not (
        profile.row_count >= 20
        and profile.physical_column_count >= 2
        and profile.measure_candidate_count == 1
        and profile.temporal_order_candidate_count == 1
        and profile.has_defined_grain
    ):
        return None
    return {
        "rule_id": "MET-RUNNING-010",
        "metric_type": "running_total_conceptual_metric_candidate",
        "confidence": 0.60,
        "severity": "review_required",
        "conceptual_formula": "cumulative eligible_measure ordered by eligible_time",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "measure_candidate_count": 1,
            "temporal_order_candidate_count": 1,
            "temporal_order_duplicate_count": 0,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Qual medida, ordem temporal, partição, população, período, filtros e ponto de reinício devem definir o acumulado?",
            "reason": "A regra não calcula acumulado, não seleciona campos, não decide partições ou reinícios e não gera DAX ou Power Query.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                "Definir medida, ordem temporal, partição, população, período, filtros e reinício",
                "Não recomendar esta métrica",
                "Revisar a granularidade temporal antes",
            ],
        },
    }
