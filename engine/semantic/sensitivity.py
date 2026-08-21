from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.semantic_sensitivity import SemanticSensitivityProfile


@dataclass(frozen=True)
class SemanticSensitivityColumnProfile:
    semantic_sensitivity: SemanticSensitivityProfile


def classify_sensitivity(profile: SemanticSensitivityColumnProfile) -> list[dict[str, object]]:
    data = profile.semantic_sensitivity
    if not data.header_eligible or data.non_missing_count < 1:
        return []
    return [{
        "rule_id": "SEM-SENS-015",
        "sensitivity": "personal_data_candidate",
        "confidence": 0.90,
        "evidence": {
            "header_eligible": data.header_eligible,
            "non_missing_count": data.non_missing_count,
            "basis": data.basis,
        },
        "question": {
            "text": "Esta coluna contém dado pessoal ou dado identificável que deve permanecer mascarado e receber tratamento restrito na modelagem?",
            "reason": "A classificação usa somente sinais agregados de esquema e exige validação humana para o tratamento de dados pessoais.",
            "question_type": "confirmation",
            "priority": "high",
            "blocking": True,
            "options": [],
        },
    }]
