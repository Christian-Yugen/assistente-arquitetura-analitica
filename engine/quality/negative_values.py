"""QLT-NEGATIVE-011: sinaliza negativos físicos em medidas de vocabulário fechado."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.negative_values import NORMALIZATION_BASIS, NegativeValuesProfile


Severity = Literal["low", "medium", "high"]
MINIMUM_PHYSICAL_NUMERIC_COUNT = 10


@dataclass(frozen=True)
class NegativeValuesColumnProfile:
    name: str
    negative_values: NegativeValuesProfile


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


def _is_applicable(profile: NegativeValuesColumnProfile) -> bool:
    negative_values = profile.negative_values
    if (
        not negative_values.header_eligible
        or negative_values.basis != NORMALIZATION_BASIS
        or negative_values.physical_numeric_count < MINIMUM_PHYSICAL_NUMERIC_COUNT
        or negative_values.negative_physical_count <= 0
        or negative_values.negative_physical_count > negative_values.physical_numeric_count
        or negative_values.negative_physical_ratio <= 0
    ):
        return False
    expected_ratio = round(negative_values.negative_physical_count / negative_values.physical_numeric_count, 8)
    return negative_values.negative_physical_ratio == expected_ratio


def _severity(ratio: float) -> Severity:
    if ratio <= 0.05:
        return "low"
    if ratio <= 0.20:
        return "medium"
    return "high"


def _question(severity: Severity) -> dict[str, object]:
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": False,
        "text": "Os valores negativos identificados em uma medida potencialmente não negativa representam ajustes, estornos, uma codificação válida ou erro na origem?",
        "reason": "O sinal físico é objetivo, mas sua compatibilidade com a regra de negócio exige confirmação humana antes de qualquer tratamento.",
        "options": [
            {"option_id": "valid_adjustment", "label": "Representam ajuste, estorno ou codificação válida."},
            {"option_id": "source_error", "label": "Representam possível erro na origem e precisam de correção fora desta análise."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "metrics", "report"],
    }


def evaluate_negative_values(profile: NegativeValuesColumnProfile) -> list[Finding]:
    """Emite um finding agregado; negativos são hipótese de validação, nunca correção automática."""

    if not _is_applicable(profile):
        return []
    negative_values = profile.negative_values
    severity = _severity(negative_values.negative_physical_ratio)
    severity_copy = {
        "low": ("Valor negativo potencialmente incompatível", "Um sinal negativo pode exigir interpretação de negócio antes de métricas e agregações."),
        "medium": ("Valores negativos potencialmente incompatíveis", "A recorrência do sinal pode afetar a interpretação de medidas, métricas e validações."),
        "high": ("Muitos valores negativos potencialmente incompatíveis", "A medida deve ser validada antes de sustentar inferências analíticas ou recomendações."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-NEGATIVE-PHYSICAL-COUNT", "effect": "negative", "observed_value": negative_values.negative_physical_count, "expected_condition": "negative_physical_count = 0"},
        {"code": "EVD-NEGATIVE-PHYSICAL-RATIO", "effect": "negative", "observed_ratio": negative_values.negative_physical_ratio, "expected_condition": "negative_physical_ratio = 0"},
        {"code": "EVD-NEGATIVE-PHYSICAL-BASE", "effect": "technical", "observed_value": negative_values.physical_numeric_count, "expected_condition": "physical_numeric_count >= 10"},
        {"code": "EVD-NEGATIVE-HEADER-ELIGIBILITY", "effect": "technical", "observed_value": 1, "expected_condition": "header_eligible = true"},
        {"code": "EVD-NEGATIVE-BASIS", "effect": "technical", "observed_value": negative_values.basis, "expected_condition": NORMALIZATION_BASIS},
    ]
    return [{
        "rule_id": "QLT-NEGATIVE-011",
        "category": "quality",
        "severity": severity,
        "confidence": 0.85,
        "title": severity_copy[0],
        "description": f"Foram identificados {negative_values.negative_physical_count} números físicos negativos ({negative_values.negative_physical_ratio * 100:.1f}% da base numérica elegível).",
        "impact": severity_copy[1],
        "recommendation": "Confirmar com o responsável de negócio o significado dos sinais negativos antes de definir métricas, agregações ou qualquer correção fora desta análise.",
        "evidence": evidence,
        "question": _question(severity),
    }]
