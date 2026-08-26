"""ALT-AVGAVG-008: revisão conceitual para risco já sinalizado em média de médias."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AverageOfAveragesAlertProfile:
    independent_average_of_averages_risk_signal_count: int = 0
    confirmed_average_composition_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_average_of_averages_review(profile: AverageOfAveragesAlertProfile) -> dict[str, object] | None:
    if not (
        profile.independent_average_of_averages_risk_signal_count >= 1
        and profile.confirmed_average_composition_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-AVGAVG-008",
        "category": "alert",
        "severity": "high",
        "title": "Média de médias exige revisão",
        "description": "Um sinal agregado e independente indica que a composição de médias exige confirmação humana antes do uso na modelagem.",
        "evidence": [{
            "code": "EVD-ALT-AVGAVG-INDEPENDENT-RISK-SIGNAL",
            "effect": "average_of_averages_review_required",
            "observed_value": profile.independent_average_of_averages_risk_signal_count,
            "expected_condition": "at least one independently produced aggregated average-of-averages risk signal with no confirmed composition or blocking conflict",
        }],
        "impact": "A composição de médias não deve orientar a modelagem até que sua interpretação seja confirmada por uma pessoa responsável.",
        "recommendation": "Confirmar população, peso, denominador, período e interpretação antes de usar a composição de médias.",
        "question": {
            "text": "Qual população, peso, denominador, período e interpretação foram confirmados para a composição de médias?",
            "reason": "O alerta não calcula, pondera, compara ou escolhe médias, pesos, medidas, campos ou agregações; ele exige decisão humana antes do uso.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_average_composition", "label": "Informar composição confirmada"},
                {"option_id": "defer_average_use", "label": "Adiar uso da composição até revisão"},
            ],
            "affected_modules": ["metrics", "modeling"],
        },
    }
