from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactWithoutMeasuresProfile:
    """Somente sinais independentes e agregados; nunca fato, dimensão, tabela, relação ou conteúdo de workbook."""

    independent_fact_without_measures_signal_count: int = 0
    confirmed_fact_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_fact_without_measures(profile: FactWithoutMeasuresProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_fact_without_measures_signal_count >= 1
        and profile.confirmed_fact_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []

    return [{"rule_id": "MDL-FACTNOMEAS-018", "classification_type": "fact_without_measures_review_required", "confidence": 0.0, "evidence": {"independent_fact_without_measures_signal_count": profile.independent_fact_without_measures_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Quais fatos, dimensões, entidades, tabelas, chaves, medidas e relações foram confirmados para revisão humana?", "reason": "A regra não classifica, propõe, confirma ou cria fatos sem medidas, fatos, dimensões, entidades, tabelas, chaves, relações, cardinalidades, medidas ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}]
