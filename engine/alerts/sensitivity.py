"""ALT-SENS-001: consolida um sinal agregado de sensibilidade em restrição de processamento."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SensitiveDataRestrictionProfile:
    sensitivity_signal_candidate_count: int = 0
    sensitivity_conflict_count: int = 0


def classify_sensitive_data_processing_restriction(profile: SensitiveDataRestrictionProfile) -> dict[str, object] | None:
    if profile.sensitivity_signal_candidate_count != 1 or profile.sensitivity_conflict_count > 0:
        return None
    return {
        "rule_id": "ALT-SENS-001",
        "category": "alert",
        "severity": "high",
        "title": "Restrição de processamento para sinal de dado sensível",
        "description": "Existe um único sinal agregado e independente de sensibilidade; o uso na modelagem requer revisão humana antes de qualquer processamento adicional.",
        "evidence": [{
            "code": "EVD-ALT-SENS-SIGNAL-COUNT",
            "effect": "restrictive",
            "observed_value": 1,
            "expected_condition": "exactly one independently classified aggregated sensitivity signal",
        }],
        "impact": "A coluna deve permanecer restrita até a revisão humana de privacidade e modelagem.",
        "recommendation": "Interromper o uso da coluna na modelagem e encaminhar para revisão de privacidade aprovada.",
        "question": {
            "text": "Confirma a restrição de processamento e o encaminhamento de privacidade antes de usar esta coluna na modelagem?",
            "reason": "A regra consolida apenas um sinal agregado já classificado, sem revelar categoria, campo, cabeçalho, valor ou posição.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "restrict_and_review", "label": "Confirmar restrição e encaminhar para revisão de privacidade"},
                {"option_id": "review_classification", "label": "Revisar a classificação de sensibilidade antes"},
            ],
            "affected_modules": ["privacy_review", "modeling"],
        },
    }
