"""MET-ABSDELTA-008: recomendação conceitual privada para variação absoluta."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AbsoluteDeltaConceptProfile:
    row_count: int = 0
    physical_column_count: int = 0
    actual_candidate_count: int = 0
    baseline_candidate_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_absolute_delta_concept(profile: AbsoluteDeltaConceptProfile) -> dict[str, object] | None:
    blocked = (
        profile.has_sensitive_signal
        or profile.has_formula_signal
        or profile.has_undefined_classification
        or profile.has_fact_without_grain
        or profile.classification_conflict_count > 0
        or profile.grain_ambiguity_count > 0
    )
    if blocked or not (
        profile.row_count >= 20
        and profile.physical_column_count >= 2
        and profile.actual_candidate_count == 1
        and profile.baseline_candidate_count == 1
        and profile.has_defined_grain
    ):
        return None
    return {
        "rule_id": "MET-ABSDELTA-008",
        "metric_type": "absolute_delta_conceptual_metric_candidate",
        "confidence": 0.60,
        "severity": "review_required",
        "conceptual_formula": "eligible_actual - eligible_baseline",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "actual_candidate_count": 1,
            "baseline_candidate_count": 1,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Qual medida realizada e qual referência devem definir a variação absoluta, em qual unidade, população, período e filtros?",
            "reason": "A regra não calcula variação, não seleciona campos e não gera DAX ou Power Query.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                "Definir medida realizada, referência, unidade, população, período e filtros",
                "Não recomendar esta métrica",
                "Revisar a granularidade antes",
            ],
        },
    }
