from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RepeatedAttributesProfile:
    """Somente sinais independentes e agregados; nunca atributos, tabela, relação ou conteúdo de workbook."""

    independent_repeated_attribute_signal_count: int = 0
    confirmed_attribute_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_repeated_attributes(profile: RepeatedAttributesProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_repeated_attribute_signal_count >= 1
        and profile.confirmed_attribute_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []

    return [{"rule_id": "MDL-ATTRREP-014", "classification_type": "repeated_attributes_review_required", "confidence": 0.0, "evidence": {"independent_repeated_attribute_signal_count": profile.independent_repeated_attribute_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Quais atributos, tabelas, entidades, chaves e relações foram confirmados para revisão humana?", "reason": "A regra não classifica, propõe, confirma ou cria atributos repetidos, tabelas, dimensões, entidades, fatos, chaves, relações, cardinalidades ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}]
