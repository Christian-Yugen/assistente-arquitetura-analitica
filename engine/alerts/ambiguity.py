"""ALT-AMBIG-005: bloqueio conceitual para ambiguidade estrutural sinalizada."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralAmbiguityAlertProfile:
    structural_ambiguity_signal_count: int = 0
    confirmed_unambiguous_relationship_count: int = 0
    contract_error_count: int = 0


def classify_structural_ambiguity_modeling_block(profile: StructuralAmbiguityAlertProfile) -> dict[str, object] | None:
    if not (
        profile.structural_ambiguity_signal_count >= 1
        and profile.confirmed_unambiguous_relationship_count == 0
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-AMBIG-005",
        "category": "alert",
        "severity": "high",
        "title": "Ambiguidade estrutural bloqueia a modelagem",
        "description": "Um sinal agregado de ambiguidade estrutural exige confirmação humana antes da modelagem.",
        "evidence": [{
            "code": "EVD-ALT-AMBIG-STRUCTURAL-SIGNAL",
            "effect": "modeling_blocked",
            "observed_value": profile.structural_ambiguity_signal_count,
            "expected_condition": "at least one independently inferred aggregated structural-ambiguity signal and no confirmed unambiguous relationship",
        }],
        "impact": "A modelagem deve aguardar confirmação humana da estrutura e dos relacionamentos.",
        "recommendation": "Confirmar estrutura, relações e direções antes de definir o modelo dimensional.",
        "question": {
            "text": "Qual estrutura e quais relacionamentos foram confirmados para a modelagem?",
            "reason": "O alerta não escolhe relações, caminhos ou chaves; ele exige decisão humana antes da modelagem.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_structure", "label": "Informar estrutura confirmada"},
                {"option_id": "defer_modeling", "label": "Adiar modelagem até revisão estrutural"},
            ],
            "affected_modules": ["relationships", "modeling"],
        },
    }
