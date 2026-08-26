"""ALT-SUMPCT-007: revisão conceitual para risco já sinalizado na soma de percentuais."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PercentageSumAlertProfile:
    independent_percentage_sum_risk_signal_count: int = 0
    confirmed_percentage_composition_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_percentage_sum_review(profile: PercentageSumAlertProfile) -> dict[str, object] | None:
    if not (
        profile.independent_percentage_sum_risk_signal_count >= 1
        and profile.confirmed_percentage_composition_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-SUMPCT-007",
        "category": "alert",
        "severity": "high",
        "title": "Soma de percentuais exige revisão",
        "description": "Um sinal agregado e independente indica que a composição percentual exige confirmação humana antes do uso na modelagem.",
        "evidence": [{
            "code": "EVD-ALT-SUMPCT-INDEPENDENT-RISK-SIGNAL",
            "effect": "percentage_sum_review_required",
            "observed_value": profile.independent_percentage_sum_risk_signal_count,
            "expected_condition": "at least one independently produced aggregated percentage-sum risk signal with no confirmed composition or blocking conflict",
        }],
        "impact": "A composição percentual não deve orientar a modelagem até que sua interpretação seja confirmada por uma pessoa responsável.",
        "recommendation": "Confirmar denominador, população, período, sobreposição e interpretação antes de usar a composição percentual.",
        "question": {
            "text": "Qual denominador, população, período, sobreposição e interpretação foram confirmados para a composição percentual?",
            "reason": "O alerta não identifica, soma, escolhe ou calcula percentuais, medidas, campos ou agregações; ele exige decisão humana antes do uso.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_percentage_composition", "label": "Informar composição confirmada"},
                {"option_id": "defer_percentage_use", "label": "Adiar uso da composição até revisão"},
            ],
            "affected_modules": ["metrics", "modeling"],
        },
    }
