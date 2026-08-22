"""SEM-DESC-004: hipótese conservadora de nome ou descrição."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_description import SemanticDescriptionProfile
from engine.profiling.semantic_identifier import SemanticIdentifierProfile


@dataclass(frozen=True)
class SemanticDescriptionColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    semantic_date: SemanticDateProfile
    semantic_identifier: SemanticIdentifierProfile
    semantic_description: SemanticDescriptionProfile


def classify_name_or_description(profile: SemanticDescriptionColumnProfile) -> list[dict[str, object]]:
    """Emite uma hipótese bloqueante somente a partir de sinais agregados autorizados."""

    description = profile.semantic_description
    identifiers = profile.semantic_identifier
    dates = profile.semantic_date
    if (
        not description.header_eligible
        or identifiers.non_missing_count < 10
        or profile.physical_type != "text"
        or profile.formulas.formula_count != 0
        or dates.recognized_date_count != 0
        or identifiers.distinct_non_missing_count < 2
        or identifiers.distinct_ratio < 0.20
    ):
        return []
    return [{
        "rule_id": "SEM-DESC-004",
        "semantic_type": "name_or_description_candidate",
        "confidence": 0.70,
        "evidence": {
            "header_eligible": description.header_eligible,
            "non_missing_count": identifiers.non_missing_count,
            "physical_type": profile.physical_type,
            "formula_count": profile.formulas.formula_count,
            "recognized_date_count": dates.recognized_date_count,
            "distinct_non_missing_count": identifiers.distinct_non_missing_count,
            "distinct_ratio": identifiers.distinct_ratio,
            "basis": description.basis,
        },
        "question": {
            "text": "A coluna deve ser tratada como nome ou descrição e, quando aplicável, validada também como possível dado pessoal?",
            "reason": "A hipótese usa vocabulário fechado e sinais físicos agregados; o significado de negócio e a política de privacidade exigem validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
