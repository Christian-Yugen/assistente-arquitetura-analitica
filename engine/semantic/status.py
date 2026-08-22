"""SEM-STATUS-009: hipótese conservadora de status textual."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_description import SemanticDescriptionProfile
from engine.profiling.semantic_identifier import SemanticIdentifierProfile
from engine.profiling.semantic_status import SemanticStatusProfile


@dataclass(frozen=True)
class SemanticStatusColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    semantic_date: SemanticDateProfile
    semantic_identifier: SemanticIdentifierProfile
    semantic_description: SemanticDescriptionProfile
    semantic_status: SemanticStatusProfile


def classify_status(profile: SemanticStatusColumnProfile) -> list[dict[str, object]]:
    """Emite status somente a partir de cabeçalho fechado e evidências estruturais agregadas."""

    status = profile.semantic_status
    identifiers = profile.semantic_identifier
    dates = profile.semantic_date
    if (
        not status.header_eligible
        or profile.semantic_description.header_eligible
        or identifiers.non_missing_count < 10
        or profile.physical_type != "text"
        or status.physical_text_count != identifiers.non_missing_count
        or not 2 <= identifiers.distinct_non_missing_count <= 12
        or identifiers.distinct_ratio > 0.50
        or profile.formulas.formula_count != 0
        or dates.recognized_date_count != 0
        or status.ambiguity_count != 0
    ):
        return []
    return [{
        "rule_id": "SEM-STATUS-009",
        "semantic_type": "status_candidate",
        "confidence": 0.75,
        "evidence": {
            "header_eligible": status.header_eligible,
            "non_missing_count": identifiers.non_missing_count,
            "physical_type": profile.physical_type,
            "physical_text_count": status.physical_text_count,
            "distinct_non_missing_count": identifiers.distinct_non_missing_count,
            "distinct_ratio": identifiers.distinct_ratio,
            "formula_count": profile.formulas.formula_count,
            "recognized_date_count": dates.recognized_date_count,
            "ambiguity_count": status.ambiguity_count,
            "basis": status.basis,
        },
        "question": {
            "text": "A coluna representa um conjunto de estados operacionais que deve ser modelado como status?",
            "reason": "A hipótese usa vocabulário fechado, textos físicos e cardinalidade apenas agregada; o significado de negócio exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
