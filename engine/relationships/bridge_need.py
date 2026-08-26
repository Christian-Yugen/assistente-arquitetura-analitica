from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BridgeNeedProfile:
    """Somente sinais independentes e agregados; nunca ponte, relacionamento, tabela ou conteúdo de workbook."""

    independent_bridge_need_signal_count: int = 0
    confirmed_relationship_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_bridge_need(profile: BridgeNeedProfile) -> dict[str, object] | None:
    if not (
        profile.independent_bridge_need_signal_count >= 1
        and profile.confirmed_relationship_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None

    return {"rule_id": "REL-BRIDGE-005", "relationship_type": "bridge_need_review_required", "confidence": 0.0, "severity": "warning", "evidence": {"independent_bridge_need_signal_count": profile.independent_bridge_need_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Quais relacionamentos, tabelas, dimensões, fatos, chaves e pontes foram confirmados para revisão humana?", "reason": "A regra não detecta, recomenda, classifica, propõe, confirma ou cria necessidade de ponte, tabelas ponte, pontes, relacionamentos, dimensões, fatos, entidades, tabelas, chaves, cardinalidades ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}
