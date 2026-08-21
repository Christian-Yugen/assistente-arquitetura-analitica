"""QLT-TOTALROW-010: identifica possíveis linhas totalizadoras por aba."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.total_rows import NORMALIZATION_BASIS, TotalRowsProfile


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class TotalRowsSheetProfile:
    name: str
    total_rows: TotalRowsProfile


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


def _is_applicable(profile: TotalRowsSheetProfile) -> bool:
    total_rows = profile.total_rows
    return (
        total_rows.non_empty_row_count >= 4
        and total_rows.total_row_candidate_count > 0
        and total_rows.total_row_candidate_ratio > 0
        and total_rows.normalization_basis == NORMALIZATION_BASIS
    )


def _severity(ratio: float) -> Severity:
    if ratio <= 0.05:
        return "low"
    if ratio <= 0.20:
        return "medium"
    return "high"


def _confidence(profile: TotalRowsSheetProfile) -> float:
    return 0.90 if profile.total_rows.total_row_candidate_count == 1 else 0.95


def _question(severity: Severity) -> dict[str, object] | None:
    if severity == "low":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": severity == "high",
        "text": "As linhas agregadas identificadas representam totais ou subtotais que devem ficar fora da região analítica principal?",
        "reason": "A confirmação evita incorporar registros resumidos como se fossem eventos de detalhe ou remover separações intencionais.",
        "options": [
            {"option_id": "separate_summary_rows", "label": "São totais ou subtotais e devem ser separados da região analítica principal."},
            {"option_id": "retain_as_detail", "label": "Devem permanecer como registros de detalhe por decisão de negócio."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_total_rows(profile: TotalRowsSheetProfile) -> list[Finding]:
    """Emite um finding por aba sem revelar títulos, rótulos, valores ou posições."""

    if not _is_applicable(profile):
        return []
    total_rows = profile.total_rows
    severity = _severity(total_rows.total_row_candidate_ratio)
    severity_copy = {
        "low": ("Linha totalizadora potencial", "Um registro agregado pode distorcer conferências pontuais se for lido como detalhe."),
        "medium": ("Linhas totalizadoras potenciais", "Registros agregados podem afetar a granularidade e a preparação para consumo analítico."),
        "high": ("Muitas linhas totalizadoras potenciais", "A região tabular precisa ser validada antes de qualquer modelagem que assuma granularidade de detalhe."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-TOTALROW-COUNT", "effect": "negative", "observed_value": total_rows.total_row_candidate_count, "expected_condition": "total_row_candidate_count = 0"},
        {"code": "EVD-TOTALROW-RATIO", "effect": "negative", "observed_ratio": total_rows.total_row_candidate_ratio, "expected_condition": "total_row_candidate_ratio = 0"},
        {"code": "EVD-TOTALROW-NONEMPTY-ROWS", "effect": "technical", "observed_value": total_rows.non_empty_row_count, "expected_condition": "non_empty_row_count >= 4"},
        {"code": "EVD-TOTALROW-NORMALIZATION", "effect": "technical", "observed_value": total_rows.normalization_basis, "expected_condition": NORMALIZATION_BASIS},
    ]
    return [{
        "rule_id": "QLT-TOTALROW-010",
        "category": "quality",
        "severity": severity,
        "confidence": _confidence(profile),
        "title": severity_copy[0],
        "description": f"Foram identificadas {total_rows.total_row_candidate_count} linhas potencialmente agregadas ({total_rows.total_row_candidate_ratio * 100:.1f}% da região observada).",
        "impact": severity_copy[1],
        "recommendation": "Confirmar com o responsável de negócio se as linhas agregadas devem ser separadas da região analítica principal antes de qualquer alteração na origem.",
        "evidence": evidence,
        "question": _question(severity),
    }]
