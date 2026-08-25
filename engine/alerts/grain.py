"""ALT-GRAIN-003: bloqueio conceitual para granularidade indefinida previamente sinalizada."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UndefinedGrainAlertProfile:
    undefined_grain_signal_count: int = 0
    confirmed_grain_count: int = 0
    contract_error_count: int = 0


def classify_undefined_grain_modeling_block(profile: UndefinedGrainAlertProfile) -> dict[str, object] | None:
    if not (
        profile.undefined_grain_signal_count >= 1
        and profile.confirmed_grain_count == 0
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-GRAIN-003",
        "category": "alert",
        "severity": "high",
        "title": "Granularidade indefinida bloqueia a modelagem",
        "description": "Um sinal agregado de granularidade indefinida exige confirmação humana antes da modelagem.",
        "evidence": [{
            "code": "EVD-ALT-GRAIN-UNDEFINED-SIGNAL",
            "effect": "modeling_blocked",
            "observed_value": profile.undefined_grain_signal_count,
            "expected_condition": "at least one independently inferred aggregated undefined-grain signal and no confirmed grain",
        }],
        "impact": "A modelagem deve aguardar confirmação humana de granularidade.",
        "recommendation": "Confirmar entidade, evento, chave e unidade de análise antes de definir fatos ou dimensões.",
        "question": {
            "text": "Qual é a granularidade confirmada para a modelagem?",
            "reason": "O alerta não seleciona entidade, evento, chave ou fato; ele exige decisão humana antes da modelagem.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_grain", "label": "Informar granularidade confirmada"},
                {"option_id": "defer_modeling", "label": "Adiar modelagem até revisão de granularidade"},
            ],
            "affected_modules": ["granularity", "modeling"],
        },
    }
