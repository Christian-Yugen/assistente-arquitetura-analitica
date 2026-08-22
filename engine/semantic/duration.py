"""SEM-DUR-008: hipótese privada e conservadora de duração."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import NumericTextProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_duration import SemanticDurationProfile


@dataclass(frozen=True)
class SemanticDurationColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    numeric_text: NumericTextProfile
    semantic_date: SemanticDateProfile
    semantic_duration: SemanticDurationProfile


def classify_duration(profile: SemanticDurationColumnProfile) -> list[dict[str, object]]:
    """Emite somente hipótese bloqueante, com evidência agregada e vocabulário fechado."""

    duration = profile.semantic_duration
    if (
        not duration.header_eligible
        or profile.physical_type != "numeric"
        or duration.non_missing_count < 10
        or duration.physical_finite_numeric_count != duration.non_missing_count
        or profile.formulas.formula_count != 0
        or profile.numeric_text.numeric_text_candidate_count != 0
        or profile.numeric_text.numeric_text_ambiguity_count != 0
        or profile.semantic_date.recognized_date_count != 0
        or duration.ambiguity_count != 0
    ):
        return []
    return [{
        "rule_id": "SEM-DUR-008",
        "semantic_type": "duration_candidate",
        "confidence": 0.80,
        "evidence": {
            "header_eligible": duration.header_eligible,
            "non_missing_count": duration.non_missing_count,
            "physical_finite_numeric_count": duration.physical_finite_numeric_count,
            "formula_count": profile.formulas.formula_count,
            "numeric_text_candidate_count": profile.numeric_text.numeric_text_candidate_count,
            "numeric_text_ambiguity_count": profile.numeric_text.numeric_text_ambiguity_count,
            "recognized_date_count": profile.semantic_date.recognized_date_count,
            "ambiguity_count": duration.ambiguity_count,
            "basis": duration.basis,
        },
        "question": {
            "text": "Esta coluna representa uma duração na unidade explicitamente indicada no cabeçalho, e não uma quantidade, prazo, data ou outra medida?",
            "reason": "A hipótese usa vocabulário fechado e sinais físicos agregados; o significado de negócio exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
