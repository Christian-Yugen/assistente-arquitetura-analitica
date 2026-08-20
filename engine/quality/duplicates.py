"""QLT-DUP-002: revela linhas integralmente repetidas sem inferir chaves de negócio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.duplicate_rows import DuplicateRowsProfile, NORMALIZATION_BASIS


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class DuplicateRowsSheetProfile:
    name: str
    duplicates: DuplicateRowsProfile


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


def _is_applicable(profile: DuplicateRowsSheetProfile) -> bool:
    duplicates = profile.duplicates
    return (
        duplicates.non_empty_row_count >= 2
        and duplicates.duplicate_group_count > 0
        and duplicates.duplicate_row_count >= 2
        and duplicates.duplicate_row_ratio > 0
        and duplicates.normalization_basis == NORMALIZATION_BASIS
    )


def _severity(ratio: float) -> Severity:
    if ratio < 0.05:
        return "low"
    if ratio < 0.2:
        return "medium"
    return "high"


def _confidence(profile: DuplicateRowsSheetProfile) -> float:
    duplicates = profile.duplicates
    penalty = 0.14 if duplicates.non_empty_row_count == 2 else 0.0
    penalty = max(penalty, 0.10 if duplicates.largest_duplicate_group > 100 else 0.0)
    return round(max(0.5, 0.92 - penalty), 2)


def _question(profile: DuplicateRowsSheetProfile, severity: Severity) -> dict[str, object] | None:
    if severity != "high":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high",
        "blocking": True,
        "text": (
            f"A {profile.name} possui linhas integralmente repetidas em parcela relevante dos registros. "
            "Essas linhas representam duplicidade operacional?"
        ),
        "reason": "A confirmação impede retenção ou deduplicação indevida de eventos legitimamente repetidos.",
        "options": [
            {"option_id": "operational_duplicates", "label": "Representam duplicidade operacional e devem ser tratadas na origem com regra aprovada."},
            {"option_id": "distinct_events", "label": "Representam eventos distintos e devem ser preservadas."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_duplicate_rows(profile: DuplicateRowsSheetProfile) -> list[Finding]:
    """Emite evidência de duplicidade integral sem revelar linhas ou sugerir exclusão."""

    if not _is_applicable(profile):
        return []
    duplicates = profile.duplicates
    severity = _severity(duplicates.duplicate_row_ratio)
    severity_copy = {
        "low": ("Poucas linhas integralmente repetidas", "A repetição pode afetar conferências pontuais e merece investigação de origem."),
        "medium": ("Linhas integralmente repetidas", "A repetição pode distorcer contagens, agregações e medidas dependentes do volume de registros."),
        "high": ("Repetição frequente de linhas", "A confirmação de negócio é necessária antes de qualquer retenção ou deduplicação."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-DUP-GROUPS", "effect": "negative", "observed_value": duplicates.duplicate_group_count, "expected_condition": "duplicate_group_count = 0"},
        {"code": "EVD-DUP-ROWS", "effect": "negative", "observed_value": duplicates.duplicate_row_count, "expected_condition": "duplicate_row_count = 0"},
        {"code": "EVD-DUP-RATIO", "effect": "negative", "observed_value": duplicates.duplicate_row_ratio, "expected_condition": "duplicate_row_ratio = 0"},
        {"code": "EVD-DUP-LARGEST-GROUP", "effect": "technical", "observed_value": duplicates.largest_duplicate_group, "expected_condition": "largest_duplicate_group = 0"},
        {"code": "EVD-DUP-NORMALIZATION", "effect": "technical", "observed_value": duplicates.normalization_basis, "expected_condition": NORMALIZATION_BASIS},
    ]
    return [{
        "rule_id": "QLT-DUP-002",
        "category": "quality",
        "severity": severity,
        "confidence": _confidence(profile),
        "title": severity_copy[0],
        "description": (
            f"A {profile.name} possui {duplicates.duplicate_group_count} grupos de linhas integralmente repetidas, "
            f"afetando {duplicates.duplicate_row_count} linhas ({duplicates.duplicate_row_ratio * 100:.1f}%)."
        ),
        "impact": severity_copy[1],
        "recommendation": "Investigar a origem das linhas integralmente repetidas e definir com o responsável de negócio se há duplicidade operacional antes de qualquer retenção ou deduplicação.",
        "evidence": evidence,
        "question": _question(profile, severity),
    }]
