"""SEM-CURR-006: classificação privada e conservadora de valor monetário."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import NumericTextProfile
from engine.profiling.semantic_currency import SemanticCurrencyProfile
from engine.profiling.semantic_date import SemanticDateProfile


@dataclass(frozen=True)
class SemanticCurrencyColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    numeric_text: NumericTextProfile
    semantic_date: SemanticDateProfile
    semantic_currency: SemanticCurrencyProfile


def classify_currency(profile: SemanticCurrencyColumnProfile) -> list[dict[str, object]]:
    data = profile.semantic_currency
    if (
        not data.header_eligible
        or profile.physical_type != "numeric"
        or data.physical_numeric_count < 10
        or data.currency_format_numeric_count != data.physical_numeric_count
        or profile.formulas.formula_count > 0
        or profile.numeric_text.numeric_text_candidate_count > 0
        or profile.numeric_text.numeric_text_ambiguity_count > 0
        or profile.semantic_date.recognized_date_ratio == 1.0
    ):
        return []
    return [{
        "rule_id": "SEM-CURR-006",
        "semantic_type": "currency_candidate",
        "confidence": 0.80,
        "evidence": {
            "header_eligible": data.header_eligible,
            "physical_numeric_count": data.physical_numeric_count,
            "currency_format_numeric_count": data.currency_format_numeric_count,
            "formula_count": profile.formulas.formula_count,
            "numeric_text_candidate_count": profile.numeric_text.numeric_text_candidate_count,
            "numeric_text_ambiguity_count": profile.numeric_text.numeric_text_ambiguity_count,
            "recognized_date_ratio": profile.semantic_date.recognized_date_ratio,
            "basis": data.basis,
        },
        "question": {
            "text": "Esta coluna representa montantes monetários; a moeda e a unidade de negócio exibidas estão corretas para a modelagem?",
            "reason": "A classificação usa sinais privados e fechados; moeda, unidade e finalidade de negócio exigem validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
