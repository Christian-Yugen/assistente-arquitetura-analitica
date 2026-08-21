"""SEM-DATE-001: classificação conservadora de coluna de data genérica."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.semantic_date import SemanticDateProfile


@dataclass(frozen=True)
class SemanticDateColumnProfile:
    name: str
    semantic_date: SemanticDateProfile


def classify_date_generic(profile: SemanticDateColumnProfile) -> list[dict[str, object]]:
    data = profile.semantic_date
    if data.non_missing_count < 10 or data.recognized_date_ratio != 1.0:
        return []
    return [{
        "rule_id": "SEM-DATE-001", "semantic_type": "date_generic", "confidence": 0.85,
        "evidence": {"non_missing_count": data.non_missing_count, "recognized_date_count": data.recognized_date_count,
                     "recognized_date_ratio": data.recognized_date_ratio, "physical_date_count": data.physical_date_count,
                     "iso_text_count": data.iso_text_count, "br_hyphen_text_count": data.br_hyphen_text_count,
                     "br_slash_text_count": data.br_slash_text_count, "basis": data.basis},
        "question": {"text": "Esta coluna deve ser tratada como uma data genérica no modelo analítico?",
                     "reason": "A classificação usa somente cobertura integral por formatos estritos; a finalidade de negócio exige validação humana.",
                     "question_type": "confirmation", "priority": "low", "blocking": False, "options": []},
    }]
