from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PreAggregationProfile:
    """Somente sinais independentes e agregados; nunca métricas, níveis de detalhe ou conteúdo de workbook."""

    independent_pre_aggregation_signal_count: int = 0
    confirmed_pre_aggregation_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_pre_aggregation(profile: PreAggregationProfile) -> dict[str, object] | None:
    if not (
        profile.independent_pre_aggregation_signal_count >= 1
        and profile.confirmed_pre_aggregation_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None

    return {
        "rule_id": "GRN-PREAGG-008",
        "category": "grain",
        "severity": "high",
        "title": "Possível agregação prévia exige revisão",
        "description": "Um sinal agregado e independente exige confirmação humana antes de tratar a estrutura como agregada previamente.",
        "evidence": [{"code": "EVD-GRN-PREAGG-INDEPENDENT-SIGNAL", "effect": "pre_aggregation_review_required", "observed_value": profile.independent_pre_aggregation_signal_count, "expected_condition": "at least one independently produced aggregated pre-aggregation signal without confirmation or blocking conflict"}],
        "impact": "A estrutura não deve orientar a modelagem até confirmação humana.",
        "recommendation": "Confirmar o nível de detalhe, a agregação prévia, a entidade ou evento e a chave antes da modelagem.",
        "question": {"text": "Qual nível de detalhe, agregação prévia, entidade ou evento e chave foram confirmados para esta estrutura?", "reason": "A regra não infere, calcula, soma, conta, compara, recomputa, seleciona ou desagrega métricas, medidas, níveis de detalhe, entidades, eventos, chaves, fatos, dimensões, relações ou campos.", "question_type": "single_choice", "priority": "high", "blocking": True, "options": [{"option_id": "confirm_pre_aggregation", "label": "Informar agregação prévia confirmada"}, {"option_id": "defer_modeling", "label": "Adiar modelagem até revisão"}], "affected_modules": ["grain", "modeling"]},
    }
