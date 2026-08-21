"""QLT-BADDATE-006: datas inválidas em formatos estritos ISO e brasileiros aprovados."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.bad_dates import BadDateProfile, NORMALIZATION_BASIS


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class BadDateColumnProfile:
    """O nome atende ao contexto do executor, mas nunca é serializado pela regra."""

    name: str
    bad_dates: BadDateProfile


class Finding(TypedDict):
    rule_id: str
    category: str
    severity: Severity
    confidence: float
    title: str
    description: str
    impact: str
    recommendation: str
    evidence: list[dict[str, object]]
    question: dict[str, object] | None


def _is_applicable(profile: BadDateProfile) -> bool:
    return (
        profile.normalization_basis == NORMALIZATION_BASIS
        and profile.strict_date_candidate_count > 0
        and 0 < profile.invalid_strict_date_count <= profile.strict_date_candidate_count
        and profile.invalid_strict_date_ratio == round(profile.invalid_strict_date_count / profile.strict_date_candidate_count, 8)
    )


def _severity(invalid_ratio: float) -> Severity:
    if invalid_ratio <= 0.05:
        return "low"
    if invalid_ratio <= 0.20:
        return "medium"
    return "high"


def _question(severity: Severity) -> dict[str, object] | None:
    if severity == "low":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": severity == "high",
        "text": "Os textos de data em formato estrito contêm valores que não correspondem ao calendário. A origem deve corrigi-los ou confirmar uma exceção de negócio?",
        "reason": "A validação humana evita correção automática de datas e interpretações de formato não autorizadas.",
        "options": [
            {"option_id": "correct_source", "label": "Corrigir os valores na origem após validação."},
            {"option_id": "business_exception", "label": "Registrar uma exceção de negócio e tratar explicitamente."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_bad_dates(profile: BadDateColumnProfile) -> list[Finding]:
    """Emite no máximo um finding agregado, sem valores, posições ou identificadores da coluna."""

    bad_dates = profile.bad_dates
    if not _is_applicable(bad_dates):
        return []
    severity = _severity(bad_dates.invalid_strict_date_ratio)
    evidence: list[dict[str, object]] = [
        {
            "code": "EVD-BADDATE-CANDIDATES",
            "effect": "technical",
            "observed_value": bad_dates.strict_date_candidate_count,
            "expected_condition": "strict_date_candidate_count > 0",
        },
        {
            "code": "EVD-BADDATE-INVALID",
            "effect": "negative",
            "observed_value": bad_dates.invalid_strict_date_count,
            "expected_condition": "invalid_strict_date_count = 0",
        },
        {
            "code": "EVD-BADDATE-RATIO",
            "effect": "negative",
            "observed_ratio": bad_dates.invalid_strict_date_ratio,
            "expected_condition": "invalid_strict_date_ratio <= 0.05",
        },
        {
            "code": "EVD-BADDATE-NORMALIZATION",
            "effect": "technical",
            "observed_value": bad_dates.normalization_basis,
            "expected_condition": NORMALIZATION_BASIS,
        },
    ]
    return [{
        "rule_id": "QLT-BADDATE-006",
        "category": "quality",
        "severity": severity,
        "confidence": 0.98,
        "title": "Datas inválidas em formato estrito",
        "description": f"Foram identificados {bad_dates.invalid_strict_date_count} textos de data em formatos estritos que não correspondem ao calendário, sem expor valores ou identificadores.",
        "impact": "Datas inválidas podem comprometer séries temporais, filtros, relacionamentos e métricas dependentes de calendário.",
        "recommendation": "Validar e corrigir a origem após confirmação humana, sem converter automaticamente valores ou interpretar formatos fora das gramáticas aprovadas.",
        "evidence": evidence,
        "question": _question(severity),
    }]
