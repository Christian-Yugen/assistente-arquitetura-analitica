"""SEM-LOC-011: hipótese conservadora de localização textual."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_date import SemanticDateProfile
from engine.profiling.semantic_identifier import SemanticIdentifierProfile
from engine.profiling.semantic_location import SemanticLocationProfile


@dataclass(frozen=True)
class SemanticLocationColumnProfile:
    physical_type: str
    formulas: FormulaConsistencyProfile
    semantic_date: SemanticDateProfile
    semantic_identifier: SemanticIdentifierProfile
    semantic_location: SemanticLocationProfile


def classify_location(profile: SemanticLocationColumnProfile) -> list[dict[str, object]]:
    """Emite localização somente a partir de cabeçalho fechado e evidências agregadas."""

    location = profile.semantic_location
    identifiers = profile.semantic_identifier
    dates = profile.semantic_date
    if (
        not location.header_eligible
        or identifiers.non_missing_count < 10
        or profile.physical_type != "text"
        or location.physical_text_count != identifiers.non_missing_count
        or not 2 <= identifiers.distinct_non_missing_count <= 50
        or identifiers.distinct_ratio > 0.90
        or profile.formulas.formula_count != 0
        or dates.recognized_date_count != 0
        or location.ambiguity_count != 0
    ):
        return []
    return [{
        "rule_id": "SEM-LOC-011",
        "semantic_type": "location_candidate",
        "confidence": 0.75,
        "evidence": {
            "header_eligible": location.header_eligible,
            "non_missing_count": identifiers.non_missing_count,
            "physical_type": profile.physical_type,
            "physical_text_count": location.physical_text_count,
            "distinct_non_missing_count": identifiers.distinct_non_missing_count,
            "distinct_ratio": identifiers.distinct_ratio,
            "formula_count": profile.formulas.formula_count,
            "recognized_date_count": dates.recognized_date_count,
            "ambiguity_count": location.ambiguity_count,
            "basis": location.basis,
        },
        "question": {
            "text": "A coluna representa uma localização de negócio que deve ser modelada como atributo geográfico?",
            "reason": "A hipótese usa somente cabeçalho fechado, textos físicos e cardinalidade agregada; o significado de negócio exige validação humana.",
            "question_type": "confirmation",
            "priority": "medium",
            "blocking": True,
            "options": [],
        },
    }]
