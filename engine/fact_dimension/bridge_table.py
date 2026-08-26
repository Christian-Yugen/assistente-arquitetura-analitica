from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BridgeTableProfile:
    """Somente sinais independentes e agregados; nunca tabela ponte, chave, relação ou conteúdo de workbook."""

    independent_bridge_table_signal_count: int = 0
    confirmed_relationship_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_bridge_table(profile: BridgeTableProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_bridge_table_signal_count >= 1
        and profile.confirmed_relationship_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []

    return [{"rule_id": "MDL-BRIDGE-009", "classification_type": "bridge_table_review_required", "confidence": 0.0, "evidence": {"independent_bridge_table_signal_count": profile.independent_bridge_table_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Quais tabelas, entidades, chaves, cardinalidades e relações foram confirmadas?", "reason": "A regra não classifica, propõe, confirma ou cria tabelas ponte, dimensões, entidades, fatos, chaves, relações, cardinalidades, atributos ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}]
