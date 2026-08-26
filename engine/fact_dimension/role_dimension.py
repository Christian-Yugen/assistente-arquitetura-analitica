from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoleDimensionProfile:
    """Somente sinais independentes e agregados; nunca função, dimensão, chave, relação ou conteúdo de workbook."""

    independent_role_dimension_signal_count: int = 0
    confirmed_dimension_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_role_dimension(profile: RoleDimensionProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_role_dimension_signal_count >= 1
        and profile.confirmed_dimension_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []

    return [{"rule_id": "MDL-DIMROLE-007", "classification_type": "role_dimension_review_required", "confidence": 0.0, "evidence": {"independent_role_dimension_signal_count": profile.independent_role_dimension_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Qual dimensão de função, entidade, chave, atributos e relações foram confirmados?", "reason": "A regra não classifica, propõe, confirma ou cria funções, dimensões, entidades, fatos, chaves, relações, cardinalidades, atributos ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}]
