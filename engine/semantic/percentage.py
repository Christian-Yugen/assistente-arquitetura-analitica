"""SEM-PCT-007: classificação privada e conservadora de percentual."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import NumericTextProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_percentage import SemanticPercentageProfile


@dataclass(frozen=True)
class SemanticPercentageColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    numeric_text: NumericTextProfile
    semantic_date: SemanticDateProfile
    semantic_percentage: SemanticPercentageProfile


def classify_percentage(profile: SemanticPercentageColumnProfile) -> list[dict[str, object]]:
    data = profile.semantic_percentage
    if (
        not data.header_eligible
        or profile.physical_type != "numeric"
        or data.physical_numeric_count < 10
        or data.in_range_numeric_count != data.physical_numeric_count
        or profile.formulas.formula_count > 0
        or profile.numeric_text.numeric_text_candidate_count > 0
        or profile.numeric_text.numeric_text_ambiguity_count > 0
        or profile.semantic_date.recognized_date_ratio == 1.0
    ):
        return []
    return [{
        "rule_id": "SEM-PCT-007",
        "semantic_type": "percentage_candidate",
        "confidence": 0.75,
        "evidence": {
            "header_eligible": data.header_eligible,
            "physical_numeric_count": data.physical_numeric_count,
            "in_range_numeric_count": data.in_range_numeric_count,
            "formula_count": profile.formulas.formula_count,
            "numeric_text_candidate_count": profile.numeric_text.numeric_text_candidate_count,
            "numeric_text_ambiguity_count": profile.numeric_text.numeric_text_ambiguity_count,
            "recognized_date_ratio": profile.semantic_date.recognized_date_ratio,
            "basis": data.basis,
        },
        "question": {
            "text": "Esta coluna representa uma proporção ou taxa expressa de zero a um, e não uma medida, índice, código ou valor decimal de outra natureza?",
            "reason": "A classificação usa sinais privados e fechados; a finalidade de negócio exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
