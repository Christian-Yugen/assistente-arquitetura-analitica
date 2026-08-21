"""QLT-NULL-001 reconstruída: detecta ausência determinística por coluna."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.missingness import MissingnessProfile
from engine.quality.numtext import Finding, Severity


RULE_ID = "QLT-NULL-001"
RULE_VERSION = "0.1.0-reconstructed.1"


@dataclass(frozen=True)
class NullColumnProfile:
    name: str
    physical_type: str
    missingness: MissingnessProfile


def _is_applicable(profile: NullColumnProfile) -> bool:
    missingness = profile.missingness
    return (
        missingness.observed_cell_count > 0
        and missingness.non_missing_cell_count > 0
        and missingness.missing_cell_count > 0
        and missingness.non_missing_cell_count + missingness.missing_cell_count == missingness.observed_cell_count
    )


def _severity(missing_ratio: float) -> Severity:
    if missing_ratio < 0.05:
        return "low"
    if missing_ratio < 0.20:
        return "medium"
    return "high"


def _confidence(missingness: MissingnessProfile) -> float:
    base = 0.9 if missingness.observed_cell_count >= 20 else 0.6
    penalty = 0.1 if missingness.missing_class_count > 1 else 0.0
    return round(max(0.5, base - penalty), 2)


def _question(profile: NullColumnProfile, severity: Severity) -> dict[str, object] | None:
    if severity != "high" or profile.missingness.observed_cell_count < 20:
        return None
    return {
        "question_type": "single_choice",
        "priority": "high",
        "blocking": True,
        "text": (
            f"A coluna {profile.name} possui uma proporção alta de valores ausentes. "
            "A ausência é esperada pelo processo de negócio, representa erro de qualidade ou ainda não é possível confirmar?"
        ),
        "reason": "A resposta define se a modelagem deve preservar a ausência, aplicar regra de qualidade ou criar tratamento explícito.",
        "options": [
            {"option_id": "expected_missingness", "label": "A ausência é esperada pelo processo de negócio."},
            {"option_id": "quality_error", "label": "A ausência representa erro de qualidade a ser corrigido."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "modeling", "metrics", "report"],
    }


def evaluate_nulls(profile: NullColumnProfile) -> list[Finding]:
    """Produz finding somente com contagens, proporção e classes de ausência aprovadas."""

    if not _is_applicable(profile):
        return []

    missingness = profile.missingness
    severity = _severity(missingness.missing_ratio)
    percentage = f"{missingness.missing_ratio * 100:.1f}%"
    evidence: list[dict[str, object]] = [
        {
            "code": "EVD-NULL-OBSERVED-CELL-COUNT",
            "effect": "context",
            "observed_value": missingness.observed_cell_count,
            "expected_condition": "observed_cell_count > 0",
        },
        {
            "code": "EVD-NULL-MISSING-CELL-COUNT",
            "effect": "negative",
            "observed_value": missingness.missing_cell_count,
            "expected_condition": "missing_cell_count = 0",
        },
        {
            "code": "EVD-NULL-MISSING-RATIO",
            "effect": "negative",
            "observed_value": missingness.missing_ratio,
            "expected_condition": "missing_ratio < 0.05",
        },
        {
            "code": "EVD-NULL-CLASS-BREAKDOWN",
            "effect": "technical",
            "observed_value": {
                "structural_null_count": missingness.structural_null_count,
                "blank_text_count": missingness.blank_text_count,
                "numeric_nan_count": missingness.numeric_nan_count,
            },
            "expected_condition": "structural_null_count = blank_text_count = numeric_nan_count = 0",
        },
    ]
    copy = {
        "low": ("Poucos valores ausentes", "A ausência pontual pode exigir tratamento explícito em filtros ou métricas."),
        "medium": ("Incidência relevante de valores ausentes", "A ausência pode alterar contagens, relacionamentos e agregações se não for tratada."),
        "high": ("Proporção alta de valores ausentes", "A interpretação de negócio da ausência precisa ser confirmada antes da modelagem."),
    }[severity]
    return [
        {
            "rule_id": RULE_ID,
            "category": "quality",
            "severity": severity,
            "confidence": _confidence(missingness),
            "title": copy[0],
            "description": (
                f"A coluna {profile.name} possui {missingness.missing_cell_count} células ausentes entre "
                f"{missingness.observed_cell_count} células observadas, equivalentes a {percentage}."
            ),
            "impact": copy[1],
            "recommendation": (
                "Confirmar o significado de negócio da ausência e definir tratamento explícito antes de modelar "
                "relacionamentos, agregações ou métricas dependentes da coluna."
            ),
            "evidence": evidence,
            "question": _question(profile, severity),
        }
    ]
