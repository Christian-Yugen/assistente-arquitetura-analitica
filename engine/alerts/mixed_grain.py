"""ALT-MIXGRAIN-009: revisão conceitual para risco já sinalizado de mistura de granularidades."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MixedGrainAlertProfile:
    independent_mixed_grain_signal_count: int = 0
    confirmed_single_grain_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_mixed_grain_review(profile: MixedGrainAlertProfile) -> dict[str, object] | None:
    if not (
        profile.independent_mixed_grain_signal_count >= 1
        and profile.confirmed_single_grain_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-MIXGRAIN-009",
        "category": "alert",
        "severity": "high",
        "title": "Mistura de granularidades exige revisão",
        "description": "Um sinal agregado e independente indica que a granularidade exige confirmação humana antes do uso na modelagem.",
        "evidence": [{
            "code": "EVD-ALT-MIXGRAIN-INDEPENDENT-RISK-SIGNAL",
            "effect": "mixed_grain_review_required",
            "observed_value": profile.independent_mixed_grain_signal_count,
            "expected_condition": "at least one independently produced aggregated mixed-grain risk signal with no confirmed single grain or blocking conflict",
        }],
        "impact": "A estrutura não deve orientar a modelagem até que a granularidade seja confirmada por uma pessoa responsável.",
        "recommendation": "Confirmar entidade ou evento, nível de detalhe, período e chave antes de usar a estrutura na modelagem.",
        "question": {
            "text": "Qual entidade ou evento, nível de detalhe, período e chave foram confirmados para esta estrutura?",
            "reason": "O alerta não infere, combina ou separa granularidades, entidades, eventos, chaves, fatos, dimensões, medidas ou campos; ele exige decisão humana antes do uso.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_single_grain", "label": "Informar granularidade confirmada"},
                {"option_id": "defer_structural_modeling", "label": "Adiar modelagem até revisão"},
            ],
            "affected_modules": ["grain", "modeling"],
        },
    }
