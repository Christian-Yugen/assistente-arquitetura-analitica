"""MET-SEMIADD-012: recomendação conceitual privada para medida semiaditiva."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SemiadditiveConceptProfile:
    row_count: int = 0
    physical_column_count: int = 0
    potential_balance_candidate_count: int = 0
    temporal_order_candidate_count: int = 0
    temporal_order_duplicate_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_semiadditive_concept(profile: SemiadditiveConceptProfile) -> dict[str, object] | None:
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
        and profile.potential_balance_candidate_count == 1
        and profile.temporal_order_candidate_count == 1
        and profile.has_defined_grain
    ):
        return None
    return {
        "rule_id": "MET-SEMIADD-012",
        "metric_type": "semiadditive_conceptual_metric_candidate",
        "confidence": 0.60,
        "severity": "review_required",
        "conceptual_formula": "aggregate eligible_balance across confirmed non_time_dimensions at confirmed time_grain",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "potential_balance_candidate_count": 1,
            "temporal_order_candidate_count": 1,
            "temporal_order_duplicate_count": 0,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Qual medida de saldo, dimensão temporal, dimensões não temporais, tempo de referência, agregação, população, período, filtros e unidade devem definir a semiaditividade?",
            "reason": "A regra não determina se a medida é saldo, não seleciona campos ou dimensões, não calcula agregação e não gera DAX ou Power Query.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                "Definir saldo, tempo, dimensões, agregação, população, período, filtros e unidade",
                "Não recomendar esta métrica",
                "Revisar a granularidade temporal antes",
            ],
        },
    }
