"""ALT-METRIC-006: revisão conceitual para risco de interpretação já sinalizado."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PotentiallyMisleadingMetricAlertProfile:
    independent_metric_risk_signal_count: int = 0
    confirmed_metric_interpretation_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_potentially_misleading_metric_review(profile: PotentiallyMisleadingMetricAlertProfile) -> dict[str, object] | None:
    if not (
        profile.independent_metric_risk_signal_count >= 1
        and profile.confirmed_metric_interpretation_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-METRIC-006",
        "category": "alert",
        "severity": "high",
        "title": "Métrica exige revisão de interpretação",
        "description": "Um sinal agregado e independente de risco de interpretação exige confirmação humana antes de usar uma métrica na modelagem.",
        "evidence": [{
            "code": "EVD-ALT-METRIC-INDEPENDENT-RISK-SIGNAL",
            "effect": "metric_interpretation_review_required",
            "observed_value": profile.independent_metric_risk_signal_count,
            "expected_condition": "at least one independently produced aggregated metric-interpretation risk signal with no confirmed interpretation or blocking conflict",
        }],
        "impact": "A métrica não deve orientar a modelagem até que sua interpretação seja confirmada por uma pessoa responsável.",
        "recommendation": "Confirmar finalidade analítica, população, unidade e interpretação antes de utilizar qualquer métrica.",
        "question": {
            "text": "Qual finalidade analítica, população, unidade e interpretação foram confirmadas para a métrica?",
            "reason": "O alerta não escolhe medida, campo, unidade, população, período, filtro ou agregação; ele exige decisão humana antes do uso da métrica.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_metric_interpretation", "label": "Informar interpretação confirmada"},
                {"option_id": "defer_metric_use", "label": "Adiar uso da métrica até revisão"},
            ],
            "affected_modules": ["metrics", "modeling"],
        },
    }
