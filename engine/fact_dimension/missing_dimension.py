from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MissingDimensionProfile:
    """Somente sinais independentes e agregados; nunca dimensão, fato, tabela, relação ou conteúdo de workbook."""

    independent_missing_dimension_signal_count: int = 0
    confirmed_dimension_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_missing_dimension(profile: MissingDimensionProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_missing_dimension_signal_count >= 1
        and profile.confirmed_dimension_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []

    return [{"rule_id": "MDL-DIMMISS-017", "classification_type": "missing_dimension_review_required", "confidence": 0.0, "evidence": {"independent_missing_dimension_signal_count": profile.independent_missing_dimension_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Quais dimensões, fatos, entidades, tabelas, chaves e relações foram confirmados para revisão humana?", "reason": "A regra não classifica, propõe, confirma ou cria dimensões ausentes, dimensões, fatos, entidades, tabelas, chaves, relações, cardinalidades ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}]
