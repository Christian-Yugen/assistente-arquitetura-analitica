from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DegenerateDimensionProfile:
    """Somente sinais independentes e agregados; nunca dimensão degenerada, chave, relação ou conteúdo de workbook."""

    independent_degenerate_dimension_signal_count: int = 0
    confirmed_dimension_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_degenerate_dimension(profile: DegenerateDimensionProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_degenerate_dimension_signal_count >= 1
        and profile.confirmed_dimension_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []

    return [{"rule_id": "MDL-DIMDEG-008", "classification_type": "degenerate_dimension_review_required", "confidence": 0.0, "evidence": {"independent_degenerate_dimension_signal_count": profile.independent_degenerate_dimension_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Qual dimensão degenerada, entidade, chave, atributos e relações foram confirmados?", "reason": "A regra não classifica, propõe, confirma ou cria dimensões degeneradas, dimensões, entidades, fatos, chaves, relações, cardinalidades, atributos ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}]
