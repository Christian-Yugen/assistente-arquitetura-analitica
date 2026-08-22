"""SEM-COMP-002: hipótese conservadora de data de competência."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_competence import SemanticCompetenceProfile
from engine.profiling.semantic_date import SemanticDateProfile


@dataclass(frozen=True)
class SemanticCompetenceColumnProfile:
    formulas: FormulaConsistencyProfile
    semantic_date: SemanticDateProfile
    semantic_competence: SemanticCompetenceProfile


def classify_competence_date(profile: SemanticCompetenceColumnProfile) -> list[dict[str, object]]:
    """Emite apenas uma hipótese bloqueante baseada em sinais agregados autorizados."""

    competence = profile.semantic_competence
    dates = profile.semantic_date
    if (
        not competence.header_eligible
        or dates.non_missing_count < 10
        or dates.recognized_date_ratio != 1.0
        or profile.formulas.formula_count != 0
    ):
        return []
    return [{
        "rule_id": "SEM-COMP-002",
        "semantic_type": "competence_date_candidate",
        "confidence": 0.85,
        "evidence": {
            "header_eligible": competence.header_eligible,
            "non_missing_count": dates.non_missing_count,
            "recognized_date_count": dates.recognized_date_count,
            "recognized_date_ratio": dates.recognized_date_ratio,
            "formula_count": profile.formulas.formula_count,
            "basis": competence.basis,
        },
        "question": {
            "text": "Esta coluna representa uma data de competência que deve orientar a periodização analítica?",
            "reason": "A classificação combina vocabulário fechado e cobertura integral de datas estritas; o significado de negócio exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
