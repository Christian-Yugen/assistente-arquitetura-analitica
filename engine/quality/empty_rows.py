"""QLT-EMPTYROW-004: identifica somente linhas vazias internas por aba."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.empty_rows import EmptyRowsProfile, NORMALIZATION_BASIS


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class EmptyRowsSheetProfile:
    name: str
    empty_rows: EmptyRowsProfile


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


def _is_applicable(profile: EmptyRowsSheetProfile) -> bool:
    empty_rows = profile.empty_rows
    return (
        empty_rows.non_empty_row_count >= 2
        and empty_rows.empty_row_count > 0
        and empty_rows.empty_row_ratio > 0
        and empty_rows.normalization_basis == NORMALIZATION_BASIS
    )


def _severity(ratio: float) -> Severity:
    if ratio < 0.05:
        return "low"
    if ratio < 0.20:
        return "medium"
    return "high"


def _confidence(profile: EmptyRowsSheetProfile) -> float:
    return 0.80 if profile.empty_rows.non_empty_row_count == 2 else 0.95


def _question(profile: EmptyRowsSheetProfile, severity: Severity) -> dict[str, object] | None:
    if severity != "high":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high",
        "blocking": True,
        "text": "Foram identificados blocos internos de linhas vazias em proporção relevante. Eles são separadores intencionais?",
        "reason": "A confirmação evita tratar como falha uma separação operacional ou, no sentido inverso, ignorar uma lacuna de extração.",
        "options": [
            {"option_id": "intentional_separators", "label": "São separadores intencionais e devem ser preservados."},
            {"option_id": "unintended_gaps", "label": "São lacunas não intencionais e devem ser corrigidas na origem após validação."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_empty_rows(profile: EmptyRowsSheetProfile) -> list[Finding]:
    """Emite um finding por aba sem revelar posições, títulos brutos ou valores de células."""

    if not _is_applicable(profile):
        return []
    empty_rows = profile.empty_rows
    severity = _severity(empty_rows.empty_row_ratio)
    severity_copy = {
        "low": ("Poucas linhas vazias entre registros", "A lacuna pode interromper conferências pontuais e merece revisão de origem."),
        "medium": ("Linhas vazias entre registros", "A descontinuidade pode afetar a leitura tabular, validações e a preparação para consumo analítico."),
        "high": ("Muitas linhas vazias entre registros", "A continuidade da região tabular precisa ser confirmada antes de qualquer preparação ou modelagem dependente."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-EMPTYROW-COUNT", "effect": "negative", "observed_value": empty_rows.empty_row_count, "expected_condition": "internal_empty_row_count = 0"},
        {"code": "EVD-EMPTYROW-RATIO", "effect": "negative", "observed_ratio": empty_rows.empty_row_ratio, "expected_condition": "internal_empty_row_ratio = 0"},
        {"code": "EVD-EMPTYROW-BLOCKS", "effect": "technical", "observed_value": empty_rows.empty_row_block_count, "expected_condition": "internal_empty_row_block_count = 0"},
        {"code": "EVD-EMPTYROW-NONEMPTY-ROWS", "effect": "technical", "observed_value": empty_rows.non_empty_row_count, "expected_condition": "non_empty_row_count >= 2"},
        {"code": "EVD-EMPTYROW-NORMALIZATION", "effect": "technical", "observed_value": empty_rows.normalization_basis, "expected_condition": NORMALIZATION_BASIS},
    ]
    return [{
        "rule_id": "QLT-EMPTYROW-004",
        "category": "quality",
        "severity": severity,
        "confidence": _confidence(profile),
        "title": severity_copy[0],
        "description": (
            f"Foram identificadas {empty_rows.empty_row_count} linhas vazias em "
            f"{empty_rows.empty_row_block_count} blocos internos ({empty_rows.empty_row_ratio * 100:.1f}% da região observada)."
        ),
        "impact": severity_copy[1],
        "recommendation": "Confirmar com o responsável de negócio se os blocos são separadores intencionais ou lacunas de extração antes de qualquer alteração na origem.",
        "evidence": evidence,
        "question": _question(profile, severity),
    }]
