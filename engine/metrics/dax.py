"""MET-DAX-015: template DAX abstrato, privado e dependente de confirmação humana."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DaxTemplateConceptProfile:
    row_count: int = 0
    physical_column_count: int = 0
    confirmed_conceptual_formula_count: int = 0
    human_confirmation_count: int = 0
    has_defined_grain: bool = False
    grain_ambiguity_count: int = 0
    has_undefined_classification: bool = False
    has_fact_without_grain: bool = False
    classification_conflict_count: int = 0
    has_sensitive_signal: bool = False
    has_formula_signal: bool = False


def classify_dax_template_concept(profile: DaxTemplateConceptProfile) -> dict[str, object] | None:
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
        and profile.confirmed_conceptual_formula_count == 1
        and profile.human_confirmation_count == 1
        and profile.has_defined_grain
    ):
        return None
    return {
        "rule_id": "MET-DAX-015",
        "metric_type": "dax_template_review_required",
        "confidence": 0.55,
        "severity": "review_required",
        "conceptual_formula": "SUM([CONFIRMED_MEASURE])",
        "evidence": {
            "row_count": profile.row_count,
            "physical_column_count": profile.physical_column_count,
            "confirmed_conceptual_formula_count": 1,
            "human_confirmation_count": 1,
            "has_defined_grain": True,
        },
        "question": {
            "text": "Confirma a intenção da medida e a substituição humana do token [CONFIRMED_MEASURE] antes de usar este template DAX?",
            "reason": "O template é abstrato, não seleciona campos nem valida ou executa DAX contra o modelo.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                "Confirmar intenção e substituir manualmente o token",
                "Não usar template DAX",
                "Revisar fórmula conceitual ou granularidade antes",
            ],
        },
    }
