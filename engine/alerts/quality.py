"""ALT-QUALITY-002: consolida risco técnico a partir de findings de qualidade agregados."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CriticalQualityRiskProfile:
    high_quality_finding_count: int = 0
    distinct_quality_rule_count: int = 0
    analyzed_sheet_count: int = 0
    contract_error_count: int = 0


def classify_critical_quality_risk(profile: CriticalQualityRiskProfile) -> dict[str, object] | None:
    if not (
        profile.high_quality_finding_count >= 3
        and profile.distinct_quality_rule_count >= 2
        and profile.analyzed_sheet_count >= 1
        and profile.contract_error_count == 0
    ):
        return None
    return {
        "rule_id": "ALT-QUALITY-002",
        "category": "alert",
        "severity": "high",
        "title": "Risco crítico consolidado de qualidade",
        "description": "A contagem agregada de findings de qualidade altos exige priorização humana antes de ampliar a modelagem.",
        "evidence": [{
            "code": "EVD-ALT-QUALITY-AGGREGATE",
            "effect": "review_required",
            "observed_value": profile.high_quality_finding_count,
            "expected_condition": "at least three high-severity quality findings from at least two distinct quality rules",
        }, {
            "code": "EVD-ALT-QUALITY-DISTINCT-RULES",
            "effect": "review_required",
            "observed_value": profile.distinct_quality_rule_count,
            "expected_condition": "at least two distinct quality rules",
        }],
        "impact": "A modelagem deve aguardar revisão humana da qualidade agregada.",
        "recommendation": "Priorizar a revisão das regras de qualidade aplicáveis antes de ampliar o modelo.",
        "question": {
            "text": "Confirma a priorização da revisão de qualidade antes de ampliar a modelagem?",
            "reason": "O alerta consolida apenas contagens agregadas e não identifica planilhas, colunas ou conteúdo.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": [
                {"option_id": "prioritize_quality_review", "label": "Priorizar revisão de qualidade"},
                {"option_id": "accept_risk_with_governance", "label": "Registrar aceite de risco sob governança"},
            ],
            "affected_modules": ["quality_review", "modeling"],
        },
    }
