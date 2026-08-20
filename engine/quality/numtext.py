"""QLT-NUMTEXT-007: detecta valores numéricos armazenados fisicamente como texto."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class NumericTextColumnProfile:
    """Perfil mínimo, agregado e sem valores brutos necessário para a QLT-NUMTEXT-007."""

    name: str
    physical_type: Literal["text", "mixed", "numeric", "date", "boolean", "unknown"]
    non_empty_value_count: int
    numeric_text_candidate_count: int
    numeric_text_candidate_ratio: float
    numeric_text_basis: str
    numeric_text_ambiguity_count: int = 0


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


CANONICAL_NUMERIC_TEXT_BASIS = "strict_canonical_numeric_string"


def _is_applicable(profile: NumericTextColumnProfile) -> bool:
    """Evita firing sem base determinística ou em coluna já tipada como numérica."""

    return (
        profile.physical_type in {"text", "mixed"}
        and profile.non_empty_value_count > 0
        and profile.numeric_text_candidate_count > 0
        and profile.numeric_text_candidate_ratio > 0
        and profile.numeric_text_basis == CANONICAL_NUMERIC_TEXT_BASIS
    )


def _severity(ratio: float) -> Severity:
    if ratio < 0.05:
        return "low"
    if ratio < 0.5:
        return "medium"
    return "high"


def _confidence(profile: NumericTextColumnProfile) -> float:
    """Calcula confiança a partir de evidências agregadas e penaliza ambiguidade técnica."""

    ambiguity_ratio = profile.numeric_text_ambiguity_count / profile.non_empty_value_count
    penalty = 0.25 if ambiguity_ratio >= 0.1 else 0.1 if ambiguity_ratio > 0 else 0.0
    return round(max(0.5, 0.9 - penalty), 2)


def _question(profile: NumericTextColumnProfile, severity: Severity) -> dict[str, object] | None:
    if severity != "high":
        return None

    return {
        "question_type": "single_choice",
        "priority": "high",
        "blocking": True,
        "text": (
            f"A coluna {profile.name} contém valores numéricos armazenados como texto. "
            "Ela representa uma medida numérica, um identificador/código ou ainda não é possível confirmar?"
        ),
        "reason": (
            "A resposta altera a interpretação de agregações, tipos físicos, possíveis chaves e "
            "métricas derivadas."
        ),
        "options": [
            {"option_id": "numeric_measure", "label": "Representa medida numérica e deve ser convertida."},
            {"option_id": "identifier", "label": "Representa identificador/código e deve permanecer como texto."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "metrics", "report"],
    }


def evaluate_numeric_text(profile: NumericTextColumnProfile) -> list[Finding]:
    """Retorna um finding agregado; nunca expõe valores individuais da planilha."""

    if not _is_applicable(profile):
        return []

    severity = _severity(profile.numeric_text_candidate_ratio)
    percentage = f"{profile.numeric_text_candidate_ratio * 100:.1f}%"
    ambiguity_ratio = profile.numeric_text_ambiguity_count / profile.non_empty_value_count
    evidence: list[dict[str, object]] = [
        {
            "code": "EVD-NUMTEXT-COUNT",
            "effect": "negative",
            "observed_value": profile.numeric_text_candidate_count,
            "expected_condition": "numeric_text_candidate_count = 0",
        },
        {
            "code": "EVD-NUMTEXT-RATIO",
            "effect": "negative",
            "observed_value": profile.numeric_text_candidate_ratio,
            "expected_condition": "numeric_text_candidate_ratio = 0",
        },
        {
            "code": "EVD-NUMTEXT-BASIS",
            "effect": "technical",
            "observed_value": profile.numeric_text_basis,
            "expected_condition": CANONICAL_NUMERIC_TEXT_BASIS,
        },
    ]
    if profile.numeric_text_ambiguity_count:
        evidence.append(
            {
                "code": "EVD-NUMTEXT-AMBIGUITY",
                "effect": "confidence_penalty",
                "observed_value": profile.numeric_text_ambiguity_count,
                "observed_ratio": ambiguity_ratio,
                "expected_condition": "numeric_text_ambiguity_count = 0",
            }
        )

    severity_copy = {
        "low": {
            "title": "Poucos números armazenados como texto",
            "impact": "Conversões implícitas podem afetar filtros ou cálculos pontuais.",
        },
        "medium": {
            "title": "Incidência relevante de números armazenados como texto",
            "impact": "Agregações, ordenações e inferências de métrica podem ficar incorretas ou indisponíveis.",
        },
        "high": {
            "title": "Coluna majoritariamente numérica armazenada como texto",
            "impact": "A interpretação da coluna como medida, código ou chave exige validação antes da modelagem.",
        },
    }[severity]

    return [
        {
            "rule_id": "QLT-NUMTEXT-007",
            "category": "quality",
            "severity": severity,
            "confidence": _confidence(profile),
            "title": severity_copy["title"],
            "description": (
                f"A coluna {profile.name} possui {profile.numeric_text_candidate_count} valores em formato de texto "
                f"interpretáveis como número, equivalentes a {percentage} dos valores não vazios."
            ),
            "impact": severity_copy["impact"],
            "recommendation": (
                "Confirmar o significado de negócio da coluna antes de converter. Se ela representar medida, "
                "normalizar o tipo numérico com regra explícita de localidade; se representar código, preservá-la como texto."
            ),
            "evidence": evidence,
            "question": _question(profile, severity),
        }
    ]
