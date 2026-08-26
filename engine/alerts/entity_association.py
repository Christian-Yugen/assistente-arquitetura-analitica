from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EntityAssociationProfile:
    """Somente sinais independentes e agregados; nunca entidades, pares ou conteúdo de workbook."""

    independent_association_signal_count: int = 0
    confirmed_association_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_entity_association(profile: EntityAssociationProfile) -> dict[str, object] | None:
    if not (
        profile.independent_association_signal_count >= 1
        and profile.confirmed_association_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None

    return {
        "rule_id": "GRN-ASSOC-007",
        "category": "grain",
        "severity": "high",
        "title": "Possível associação entre entidades exige revisão",
        "description": "Um sinal agregado e independente exige confirmação humana antes de tratar a estrutura como associação entre entidades.",
        "evidence": [
            {
                "code": "EVD-GRN-ASSOC-INDEPENDENT-SIGNAL",
                "effect": "entity_association_review_required",
                "observed_value": profile.independent_association_signal_count,
                "expected_condition": "at least one independently produced aggregated association signal without confirmation or blocking conflict",
            }
        ],
        "impact": "A estrutura não deve orientar a modelagem até confirmação humana.",
        "recommendation": "Confirmar a associação entre entidades, o evento, a chave e o nível de detalhe antes da modelagem.",
        "question": {
            "text": "Qual associação entre entidades, evento, chave e nível de detalhe foram confirmados para esta estrutura?",
            "reason": "A regra não infere, identifica, vincula, compara ou seleciona entidades, relações, cardinalidades, eventos, chaves, fatos, dimensões ou campos.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_association", "label": "Informar associação confirmada"},
                {"option_id": "defer_modeling", "label": "Adiar modelagem até revisão"},
            ],
            "affected_modules": ["grain", "modeling"],
        },
    }
