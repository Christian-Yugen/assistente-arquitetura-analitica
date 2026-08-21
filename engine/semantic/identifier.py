"""SEM-ID-003: classificação privada e conservadora de identificadores."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.semantic_identifier import SemanticIdentifierProfile


@dataclass(frozen=True)
class SemanticIdentifierColumnProfile:
    physical_type: str
    formula_count: int
    semantic_identifier: SemanticIdentifierProfile


def classify_identifier(profile: SemanticIdentifierColumnProfile) -> list[dict[str, object]]:
    data = profile.semantic_identifier
    if (
        data.observed_count < 20
        or not data.header_signal
        or data.sensitive_header
        or profile.physical_type not in {"text", "numeric"}
        or profile.formula_count > 0
        or data.non_missing_ratio < 0.9
        or data.distinct_ratio < 0.1
    ):
        return []
    individually_unique = data.non_missing_ratio == 1.0 and data.distinct_ratio == 1.0
    return [{
        "rule_id": "SEM-ID-003", "semantic_type": "identifier", "confidence": 0.75,
        "evidence": {
            "observed_count": data.observed_count, "non_missing_count": data.non_missing_count,
            "distinct_non_missing_count": data.distinct_non_missing_count, "non_missing_ratio": data.non_missing_ratio,
            "distinct_ratio": data.distinct_ratio, "header_signal": data.header_signal,
            "individually_unique": individually_unique, "component_eligible": not individually_unique,
            "basis": data.basis,
        },
        "question": {"text": "Esta coluna representa um identificador ou componente de identificador no contexto da aba?",
                     "reason": "A classificação usa sinais agregados e não confirma a finalidade de negócio sem validação humana.",
                     "question_type": "confirmation", "priority": "low", "blocking": False, "options": []},
    }]
