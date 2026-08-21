"""SEM-QTY-005: classificação privada e conservadora de quantidade."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import NumericTextProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_quantity import SemanticQuantityProfile


@dataclass(frozen=True)
class SemanticQuantityColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    numeric_text: NumericTextProfile
    semantic_date: SemanticDateProfile
    semantic_quantity: SemanticQuantityProfile


def classify_quantity(profile: SemanticQuantityColumnProfile) -> list[dict[str, object]]:
    data = profile.semantic_quantity
    if (
        not data.header_eligible
        or profile.physical_type != "numeric"
        or data.physical_numeric_count < 10
        or profile.formulas.formula_count > 0
        or profile.numeric_text.numeric_text_candidate_count > 0
        or profile.numeric_text.numeric_text_ambiguity_count > 0
        or profile.semantic_date.recognized_date_ratio == 1.0
    ):
        return []
    return [{
        "rule_id": "SEM-QTY-005",
        "semantic_type": "quantity_candidate",
        "confidence": 0.75,
        "evidence": {
            "header_eligible": data.header_eligible,
            "physical_numeric_count": data.physical_numeric_count,
            "formula_count": profile.formulas.formula_count,
            "numeric_text_candidate_count": profile.numeric_text.numeric_text_candidate_count,
            "numeric_text_ambiguity_count": profile.numeric_text.numeric_text_ambiguity_count,
            "recognized_date_ratio": profile.semantic_date.recognized_date_ratio,
            "basis": data.basis,
        },
        "question": {
            "text": "Esta coluna representa uma quantidade física ou contagem de unidades, e não preço, saldo, código, percentual ou outra medida?",
            "reason": "A classificação usa sinais privados e fechados; a finalidade de negócio exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
