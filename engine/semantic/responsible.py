"""SEM-RESP-012: hipótese conservadora de responsável textual."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_identifier import SemanticIdentifierProfile
from engine.profiling.semantic_responsible import SemanticResponsibleProfile


@dataclass(frozen=True)
class SemanticResponsibleColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    semantic_date: SemanticDateProfile
    semantic_identifier: SemanticIdentifierProfile
    semantic_responsible: SemanticResponsibleProfile


def classify_responsible(profile: SemanticResponsibleColumnProfile) -> list[dict[str, object]]:
    """Emite responsável somente por cabeçalho fechado e evidências agregadas."""

    responsible = profile.semantic_responsible
    identifiers = profile.semantic_identifier
    dates = profile.semantic_date
    if (
        not responsible.header_eligible
        or identifiers.non_missing_count < 10
        or profile.physical_type != "text"
        or responsible.physical_text_count != identifiers.non_missing_count
        or not 2 <= identifiers.distinct_non_missing_count <= 50
        or identifiers.distinct_ratio > 0.90
        or profile.formulas.formula_count != 0
        or dates.recognized_date_count != 0
        or responsible.ambiguity_count != 0
    ):
        return []
    return [{
        "rule_id": "SEM-RESP-012",
        "semantic_type": "responsible_candidate",
        "confidence": 0.70,
        "evidence": {
            "header_eligible": responsible.header_eligible,
            "non_missing_count": identifiers.non_missing_count,
            "physical_type": profile.physical_type,
            "physical_text_count": responsible.physical_text_count,
            "distinct_non_missing_count": identifiers.distinct_non_missing_count,
            "distinct_ratio": identifiers.distinct_ratio,
            "formula_count": profile.formulas.formula_count,
            "recognized_date_count": dates.recognized_date_count,
            "ambiguity_count": responsible.ambiguity_count,
            "basis": responsible.basis,
        },
        "question": {
            "text": "A coluna representa um responsável de negócio útil ao modelo, sem pressupor natureza pessoal?",
            "reason": "A hipótese usa somente cabeçalho fechado, textos físicos e cardinalidade agregada; seu significado exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
