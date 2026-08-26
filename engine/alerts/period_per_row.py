from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PeriodPerRowProfile:
    """Somente sinais independentes e agregados; nunca conteúdo de workbook."""

    independent_period_signal_count: int = 0
    confirmed_period_per_row_count: int = 0
    structural_conflict_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0


def classify_period_per_row(profile: PeriodPerRowProfile) -> dict[str, object] | None:
    if not (
        profile.independent_period_signal_count >= 1
        and profile.confirmed_period_per_row_count == 0
        and profile.structural_conflict_count == 0
        and profile.sensitive_signal_count == 0
        and profile.contract_error_count == 0
    ):
        return None

    return {
        "rule_id": "GRN-PERIOD-005",
        "category": "grain",
        "severity": "high",
        "title": "Possível período por linha exige revisão",
        "description": "Um sinal agregado e independente exige confirmação humana antes de tratar a estrutura como período por linha.",
        "evidence": [
            {
                "code": "EVD-GRN-PERIOD-INDEPENDENT-SIGNAL",
                "effect": "period_per_row_review_required",
                "observed_value": profile.independent_period_signal_count,
                "expected_condition": "at least one independently produced aggregated period-per-row signal without confirmation or blocking conflict",
            }
        ],
        "impact": "A estrutura não deve orientar a modelagem até confirmação humana.",
        "recommendation": "Confirmar o período por linha, a referência temporal, a entidade ou evento e a chave antes da modelagem.",
        "question": {
            "text": "Qual período por linha, referência temporal, entidade ou evento e chave foram confirmados para esta estrutura?",
            "reason": "A regra não infere período, calendário, data, entidade, evento, chave, fato, dimensão, relação, medida ou campo.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "confirm_period_per_row", "label": "Informar período por linha confirmado"},
                {"option_id": "defer_modeling", "label": "Adiar modelagem até revisão"},
            ],
            "affected_modules": ["grain", "modeling"],
        },
    }
