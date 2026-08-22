"""SEM-CAT-010: hipótese conservadora de categoria textual."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_category import SemanticCategoryProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_identifier import SemanticIdentifierProfile


@dataclass(frozen=True)
class SemanticCategoryColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    semantic_date: SemanticDateProfile
    semantic_identifier: SemanticIdentifierProfile
    semantic_category: SemanticCategoryProfile


def classify_category(profile: SemanticCategoryColumnProfile) -> list[dict[str, object]]:
    """Emite categoria somente a partir de cabeçalho fechado e evidências agregadas."""

    category = profile.semantic_category
    identifiers = profile.semantic_identifier
    dates = profile.semantic_date
    if (
        not category.header_eligible
        or identifiers.non_missing_count < 10
        or profile.physical_type != "text"
        or category.physical_text_count != identifiers.non_missing_count
        or not 2 <= identifiers.distinct_non_missing_count <= 20
        or identifiers.distinct_ratio > 0.50
        or profile.formulas.formula_count != 0
        or dates.recognized_date_count != 0
        or category.ambiguity_count != 0
    ):
        return []
    return [{
        "rule_id": "SEM-CAT-010",
        "semantic_type": "category_candidate",
        "confidence": 0.70,
        "evidence": {
            "header_eligible": category.header_eligible,
            "non_missing_count": identifiers.non_missing_count,
            "physical_type": profile.physical_type,
            "physical_text_count": category.physical_text_count,
            "distinct_non_missing_count": identifiers.distinct_non_missing_count,
            "distinct_ratio": identifiers.distinct_ratio,
            "formula_count": profile.formulas.formula_count,
            "recognized_date_count": dates.recognized_date_count,
            "ambiguity_count": category.ambiguity_count,
            "basis": category.basis,
        },
        "question": {
            "text": "A coluna representa uma categorização de negócio que deve ser modelada como atributo categórico?",
            "reason": "A hipótese usa somente cabeçalho fechado, textos físicos e cardinalidade agregada; o significado de negócio exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
