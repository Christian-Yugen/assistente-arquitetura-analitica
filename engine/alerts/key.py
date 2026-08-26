"""ALT-KEY-004: bloqueio conceitual para chave inválida previamente sinalizada."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InvalidKeyAlertProfile:
    invalid_key_signal_count: int = 0
    confirmed_key_count: int = 0
    contract_error_count: int = 0


def classify_invalid_key_modeling_block(profile: InvalidKeyAlertProfile) -> dict[str, object] | None:
    if not (
        profile.invalid_key_signal_count >= 1
        and profile.confirmed_key_count == 0
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-KEY-004",
        "category": "alert",
        "severity": "high",
        "title": "Chave inválida bloqueia a modelagem",
        "description": "Um sinal agregado de chave inválida exige confirmação humana antes da modelagem.",
        "evidence": [{
            "code": "EVD-ALT-KEY-INVALID-SIGNAL",
            "effect": "modeling_blocked",
            "observed_value": profile.invalid_key_signal_count,
            "expected_condition": "at least one independently inferred aggregated invalid-key signal and no confirmed key",
        }],
        "impact": "A modelagem deve aguardar confirmação humana da chave válida.",
        "recommendation": "Confirmar a chave e sua política de integridade antes de definir relacionamentos ou fatos.",
        "question": {
            "text": "Qual é a chave confirmada para a modelagem?",
            "reason": "O alerta não detecta nem seleciona campos; ele exige decisão humana antes da modelagem.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_key", "label": "Informar chave confirmada"},
                {"option_id": "defer_modeling", "label": "Adiar modelagem até revisão de chave"},
            ],
            "affected_modules": ["relationships", "modeling"],
        },
    }
