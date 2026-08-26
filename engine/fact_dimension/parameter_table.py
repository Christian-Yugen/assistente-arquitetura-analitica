from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParameterTableProfile:
    """Somente sinais independentes e agregados; nunca tabela parâmetro, chave, relação ou conteúdo de workbook."""

    independent_parameter_table_signal_count: int = 0
    confirmed_supporting_design_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_parameter_table(profile: ParameterTableProfile) -> list[dict[str, object]]:
    if not (
        profile.independent_parameter_table_signal_count >= 1
        and profile.confirmed_supporting_design_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return []

    return [{"rule_id": "MDL-PARAM-011", "classification_type": "parameter_table_review_required", "confidence": 0.0, "evidence": {"independent_parameter_table_signal_count": profile.independent_parameter_table_signal_count, "basis": "independent_aggregate_only_fail_closed_v1"}, "question": {"text": "Quais tabelas parâmetro, tabelas auxiliares, entidades, chaves, atributos e relações foram confirmadas?", "reason": "A regra não classifica, propõe, confirma ou cria tabelas parâmetro, tabelas auxiliares, dimensões, entidades, fatos, chaves, relações, cardinalidades, atributos ou campos.", "question_type": "confirmation", "priority": "high", "blocking": True, "options": []}}]
