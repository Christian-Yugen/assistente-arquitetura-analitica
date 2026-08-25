"""MET-WAVG-011: recomendação conceitual privada para média ponderada."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeightedAverageConceptProfile:
    row_count: int = 0
    physical_column_count: int = 0
    measure_candidate_count: int = 0
    weight_candidate_count: int = 0
    nonpositive_weight_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_weighted_average_concept(profile: WeightedAverageConceptProfile) -> dict[str, object] | None:
    blocked = (
        profile.has_sensitive_signal
        or profile.has_formula_signal
        or profile.has_undefined_classification
        or profile.has_fact_without_grain
        or profile.classification_conflict_count > 0
        or profile.grain_ambiguity_count > 0
        or profile.nonpositive_weight_count > 0
    )
    if blocked or not (
        profile.row_count >= 20
        and profile.physical_column_count >= 2
        and profile.measure_candidate_count == 1
        and profile.weight_candidate_count == 1
        and profile.has_defined_grain
    ):
        return None
    return {
        "rule_id": "MET-WAVG-011",
        "metric_type": "weighted_average_conceptual_metric_candidate",
        "confidence": 0.60,
        "severity": "review_required",
        "conceptual_formula": "weighted_sum(eligible_measure, eligible_weight) / total(eligible_weight)",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "measure_candidate_count": 1,
            "weight_candidate_count": 1,
            "nonpositive_weight_count": 0,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Qual medida e qual peso estritamente positivo devem definir a média ponderada, com qual unidade, população, período, filtros, tratamento de peso e arredondamento?",
            "reason": "A regra não calcula a média ponderada, não seleciona campos, não atribui papéis e não gera DAX ou Power Query.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                "Definir medida, peso, unidade, população, período, filtros, tratamento de peso e arredondamento",
                "Não recomendar esta métrica",
                "Revisar a granularidade antes",
            ],
        },
    }
