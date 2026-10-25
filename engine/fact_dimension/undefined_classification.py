"""MDL-UNDEFINED-020: estado residual privado para classificação de tabela."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UndefinedTableClassificationSheetProfile:
    """Sinais exclusivamente agregados para o fallback de revisão humana."""

    observed_row_count: int
    physical_column_count: int
    evaluated_table_classifier_count: int
    positive_table_classification_count: int
    classification_conflict_count: int
    formula_column_count: int
    sensitive_candidate_count: int
    classification_ambiguity_count: int


def classify_undefined_table_classification(
    profile: UndefinedTableClassificationSheetProfile,
) -> list[dict[str, object]]:
    """Emite somente o estado residual draft quando nenhum classificador fechado é elegível."""

    if (
        profile.observed_row_count < 20
        or profile.physical_column_count < 2
        or profile.evaluated_table_classifier_count != 5
        or profile.positive_table_classification_count != 0
        or profile.classification_conflict_count != 0
        or profile.formula_column_count != 0
        or profile.classification_ambiguity_count != 0
    ):
        return []

    return [{
        "rule_id": "MDL-UNDEFINED-020",
        "classification_type": "table_classification_undefined_candidate",
        "confidence": 0.60,
        "evidence": {
            "observed_row_count": profile.observed_row_count,
            "physical_column_count": profile.physical_column_count,
            "evaluated_table_classifier_count": profile.evaluated_table_classifier_count,
            "positive_table_classification_count": profile.positive_table_classification_count,
            "classification_conflict_count": profile.classification_conflict_count,
            "formula_column_count": profile.formula_column_count,
            "sensitive_candidate_count": profile.sensitive_candidate_count,
            "classification_ambiguity_count": profile.classification_ambiguity_count,
            "basis": "closed_table_classification_fallback_private_v1",
        },
        "question": {
            "text": "Confirme a finalidade analítica e o grão pretendido antes de modelar esta tabela.",
            "reason": "A avaliação fechada de classificações não produziu uma hipótese elegível; este estado exige revisão humana e não conclui a semântica de negócio.",
            "question_type": "confirmation",
            "priority": "high",
            "blocking": True,
            "options": [],
        },
    }]
