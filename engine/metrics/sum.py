"""MET-SUM-002: recomendação conceitual privada para soma."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SumConceptProfile:
    """Perfil agregado sem medida, unidade, valores, cabeçalhos ou DAX."""
    row_count: int = 0
    physical_column_count: int = 0
    summable_candidate_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_sum_concept(profile: SumConceptProfile) -> dict[str, object] | None:
    """Propõe só a revisão conceitual de soma; nunca soma, escolhe medida/unidade ou gera DAX."""
    blocked = (profile.has_sensitive_signal or profile.has_formula_signal or profile.has_undefined_classification
               or profile.has_fact_without_grain or profile.classification_conflict_count > 0
               or profile.grain_ambiguity_count > 0)
    eligible = (profile.row_count >= 20 and profile.physical_column_count >= 2
                and profile.summable_candidate_count == 1 and profile.has_defined_grain)
    if blocked or not eligible:
        return None
    return {
        "rule_id": "MET-SUM-002", "metric_type": "sum_conceptual_metric_candidate",
        "confidence": 0.60, "severity": "review_required", "conceptual_formula": "SUM(eligible_measure)",
        "evidence": {"row_count": profile.row_count, "physical_column_count": profile.physical_column_count,
                     "summable_candidate_count": 1, "has_defined_grain": True},
        "question": {"text": "Qual medida deve ser somada, em qual unidade e com quais filtros de negócio?",
                     "reason": "A regra não escolhe medida ou unidade, não soma valores e não gera DAX ou Power Query.",
                     "question_type": "single_choice", "priority": "high", "blocking": True,
                     "options": ["Definir medida, unidade e filtros", "Não recomendar esta métrica", "Revisar a granularidade antes"]},
    }
