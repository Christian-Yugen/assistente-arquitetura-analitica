"""MET-COMPL-001: recomendação conceitual privada para percentual de conclusão."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompletionRateConceptProfile:
    """Perfil agregado sem valores de status, cabeçalhos, IDs de coluna ou DAX."""

    row_count: int = 0
    physical_column_count: int = 0
    status_candidate_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_completion_rate_concept(profile: CompletionRateConceptProfile) -> dict[str, object] | None:
    """Propõe somente uma fórmula conceitual; nunca calcula, escolhe estados ou gera DAX."""

    blocked = (
        profile.has_sensitive_signal
        or profile.has_formula_signal
        or profile.has_undefined_classification
        or profile.has_fact_without_grain
        or profile.classification_conflict_count > 0
        or profile.grain_ambiguity_count > 0
    )
    eligible = (
        profile.row_count >= 20
        and profile.physical_column_count >= 2
        and profile.status_candidate_count == 1
        and profile.has_defined_grain
    )
    if blocked or not eligible:
        return None

    return {
        "rule_id": "MET-COMPL-001",
        "metric_type": "completion_rate_conceptual_metric_candidate",
        "confidence": 0.60,
        "severity": "review_required",
        "conceptual_formula": "completed_items / eligible_items",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "status_candidate_count": 1,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Quais estados contam como concluídos e quais itens entram no denominador da métrica de conclusão?",
            "reason": "A regra não lê valores de status, não calcula percentual e não gera DAX ou Power Query.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": ["Definir estados e denominador", "Não recomendar esta métrica", "Revisar a granularidade antes"],
        },
    }
