"""QLT-WHITESPACE-009: sinais textuais estruturais estritamente autorizados."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.whitespace import NORMALIZATION_BASIS, WhitespaceProfile


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class WhitespaceColumnProfile:
    """O nome é aceito apenas para compatibilidade de contexto e nunca é emitido."""

    name: str
    whitespace: WhitespaceProfile


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


def _is_consistent(profile: WhitespaceProfile) -> bool:
    expected_ratio = round(profile.affected_text_count / profile.non_blank_text_count, 8) if profile.non_blank_text_count else 0.0
    return (
        all(
            count >= 0
            for count in (
                profile.non_blank_text_count,
                profile.leading_or_trailing_space_count,
                profile.hidden_character_count,
                profile.affected_text_count,
            )
        )
        and profile.affected_text_count <= profile.non_blank_text_count
        and profile.affected_text_count <= profile.leading_or_trailing_space_count + profile.hidden_character_count
        and profile.affected_text_ratio == expected_ratio
    )


def _is_applicable(profile: WhitespaceProfile) -> bool:
    return (
        profile.normalization_basis == NORMALIZATION_BASIS
        and profile.non_blank_text_count >= 3
        and profile.affected_text_count > 0
        and _is_consistent(profile)
    )


def _severity(affected_ratio: float) -> Severity:
    if affected_ratio <= 0.05:
        return "low"
    if affected_ratio <= 0.20:
        return "medium"
    return "high"


def _question(severity: Severity) -> dict[str, object] | None:
    if severity == "low":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": severity == "high",
        "text": "Os sinais textuais estruturais observados representam uma inconsistência de origem ou uma convenção intencional?",
        "reason": "A confirmação evita limpeza, normalização ou alteração indevida de dados potencialmente significativos.",
        "options": [
            {"option_id": "source_inconsistency", "label": "Representam uma inconsistência e devem ser corrigidos na origem após validação."},
            {"option_id": "intentional_convention", "label": "Representam uma convenção intencional e devem ser preservados explicitamente."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_whitespace(profile: WhitespaceColumnProfile) -> list[Finding]:
    """Emite no máximo um finding agregado, sem conteúdo ou identificadores de coluna."""

    whitespace = profile.whitespace
    if not _is_applicable(whitespace):
        return []
    severity = _severity(whitespace.affected_text_ratio)
    evidence: list[dict[str, object]] = [
        {"code": "EVD-WHITESPACE-NONBLANK", "effect": "technical", "observed_value": whitespace.non_blank_text_count, "expected_condition": "non_blank_text_count >= 3"},
        {"code": "EVD-WHITESPACE-AFFECTED", "effect": "negative", "observed_value": whitespace.affected_text_count, "expected_condition": "affected_text_count > 0"},
        {"code": "EVD-WHITESPACE-RATIO", "effect": "negative", "observed_ratio": whitespace.affected_text_ratio, "expected_condition": "affected_text_ratio > 0"},
        {"code": "EVD-WHITESPACE-MARGINAL", "effect": "technical", "observed_value": whitespace.leading_or_trailing_space_count, "expected_condition": "explicit_marginal_space_count >= 0"},
        {"code": "EVD-WHITESPACE-HIDDEN", "effect": "technical", "observed_value": whitespace.hidden_character_count, "expected_condition": "explicit_hidden_character_count >= 0"},
        {"code": "EVD-WHITESPACE-NORMALIZATION", "effect": "technical", "observed_value": whitespace.normalization_basis, "expected_condition": NORMALIZATION_BASIS},
    ]
    return [{
        "rule_id": "QLT-WHITESPACE-009",
        "category": "quality",
        "severity": severity,
        "confidence": 0.95,
        "title": "Sinais textuais estruturais observados",
        "description": "Foram observados textos com espaço marginal e/ou caractere invisível explicitamente autorizado, sem expor valores ou identificadores da coluna.",
        "impact": "Os sinais podem comprometer comparações, agrupamentos e validações técnicas se não forem confirmados na origem.",
        "recommendation": "Validar a origem e a intenção dos sinais antes de qualquer limpeza, normalização, substituição ou exclusão.",
        "evidence": evidence,
        "question": _question(severity),
    }]
