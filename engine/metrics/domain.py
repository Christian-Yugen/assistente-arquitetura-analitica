"""MET-DOMAIN-013: recomendação conceitual privada para métrica de domínio."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainMetricConceptProfile:
    row_count: int = 0
    physical_column_count: int = 0
    domain_signal_candidate_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_domain_metric_concept(profile: DomainMetricConceptProfile) -> dict[str, object] | None:
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
        and profile.domain_signal_candidate_count == 1
        and profile.has_defined_grain
    ):
        return None
    return {
        "rule_id": "MET-DOMAIN-013",
        "metric_type": "domain_metric_conceptual_metric_candidate",
        "confidence": 0.55,
        "severity": "review_required",
        "conceptual_formula": "confirmed_domain_metric",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "domain_signal_candidate_count": 1,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Qual domínio, objetivo, fórmula, medida, entidade, unidade, população, período, filtros, agregação e limites devem definir esta métrica?",
            "reason": "A regra não infere domínio de conteúdo privado, não seleciona campos, não define fórmula e não gera DAX ou Power Query.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                "Definir domínio, objetivo, fórmula, medida, entidade, unidade, população, período, filtros, agregação e limites",
                "Não recomendar esta métrica",
                "Revisar a granularidade antes",
            ],
        },
    }
