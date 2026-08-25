"""MET-IMPOSS-014: alerta conceitual agregado quando não há base para métrica revisável."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InsufficientMetricConceptProfile:
    row_count: int = 0
    physical_column_count: int = 0
    eligible_measure_candidate_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_insufficient_metric_concept(profile: InsufficientMetricConceptProfile) -> dict[str, object] | None:
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
        and profile.eligible_measure_candidate_count == 0
        and profile.has_defined_grain
    ):
        return None
    return {
        "rule_id": "MET-IMPOSS-014",
        "metric_type": "metric_insufficient_review_required",
        "confidence": 0.55,
        "severity": "review_required",
        "conceptual_formula": "no_conceptual_metric_without_confirmed_measure",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "eligible_measure_candidate_count": 0,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Existe uma medida de negócio apropriada para esta granularidade e qual é sua unidade e finalidade?",
            "reason": "A regra não afirma erro de negócio, não cria métrica, não seleciona campos e exige confirmação humana antes de qualquer sugestão.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                "Confirmar medida, unidade e finalidade de negócio",
                "Confirmar que não há medida aplicável nesta granularidade",
                "Revisar a granularidade antes",
            ],
        },
    }
