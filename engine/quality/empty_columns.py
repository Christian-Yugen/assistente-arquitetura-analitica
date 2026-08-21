"""QLT-EMPTYCOL-003: identifica colunas sem informação observável sob política conservadora."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.missingness import MissingnessProfile


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class EmptyColumnProfile:
    name: str
    missingness: MissingnessProfile


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


def _empty_count(profile: EmptyColumnProfile) -> int:
    """A opção A considera somente nulos estruturais e textos em branco."""

    missingness = profile.missingness
    return missingness.structural_null_count + missingness.blank_text_count


def _is_applicable(profile: EmptyColumnProfile) -> bool:
    missingness = profile.missingness
    return missingness.observed_cell_count > 0 and _empty_count(profile) == missingness.observed_cell_count


def _severity(observed_cell_count: int) -> Severity:
    if observed_cell_count <= 10:
        return "low"
    if observed_cell_count <= 100:
        return "medium"
    return "high"


def _confidence(observed_cell_count: int) -> float:
    return 0.80 if observed_cell_count == 1 else 0.95


def _question(profile: EmptyColumnProfile, severity: Severity) -> dict[str, object] | None:
    if severity != "high":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high",
        "blocking": True,
        "text": f"A coluna {profile.name} está vazia em todas as linhas de dados observadas. Ela possui finalidade técnica ou prevista?",
        "reason": "A confirmação impede remover ou ignorar uma coluna que possa ser preenchida por processo externo ou ter papel de negócio.",
        "options": [
            {"option_id": "technical_or_planned", "label": "Possui finalidade técnica ou prevista e deve permanecer."},
            {"option_id": "no_longer_needed", "label": "Não possui finalidade conhecida e pode ser tratada na origem após validação."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_empty_column(profile: EmptyColumnProfile) -> list[Finding]:
    """Emite um finding agregado, sem alterar ou expor a coluna avaliada."""

    if not _is_applicable(profile):
        return []
    missingness = profile.missingness
    severity = _severity(missingness.observed_cell_count)
    severity_copy = {
        "low": ("Coluna estruturalmente vazia", "A coluna não contém informação observável e deve ter sua finalidade confirmada."),
        "medium": ("Coluna estruturalmente vazia", "A coluna não contém informação observável em uma população relevante e pode confundir o consumo analítico."),
        "high": ("Coluna estruturalmente vazia em grande volume", "A finalidade da coluna precisa de confirmação antes de qualquer exclusão ou modelagem dependente."),
    }[severity]
    empty_count = _empty_count(profile)
    evidence: list[dict[str, object]] = [
        {"code": "EVD-EMPTYCOL-ROW-COUNT", "effect": "technical", "observed_value": missingness.observed_cell_count, "expected_condition": "observed_data_row_count > 0"},
        {"code": "EVD-EMPTYCOL-EMPTY-COUNT", "effect": "negative", "observed_value": empty_count, "expected_condition": "empty_cell_count < observed_data_row_count"},
        {"code": "EVD-EMPTYCOL-EMPTY-RATIO", "effect": "negative", "observed_value": 1.0, "expected_condition": "empty_cell_ratio < 1"},
        {"code": "EVD-EMPTYCOL-NUMERIC-NAN", "effect": "technical", "observed_value": missingness.numeric_nan_count, "expected_condition": "numeric_nan_count = 0"},
    ]
    return [{
        "rule_id": "QLT-EMPTYCOL-003",
        "category": "quality",
        "severity": severity,
        "confidence": _confidence(missingness.observed_cell_count),
        "title": severity_copy[0],
        "description": f"A coluna {profile.name} está vazia em {empty_count} de {missingness.observed_cell_count} linhas de dados observadas.",
        "impact": severity_copy[1],
        "recommendation": "Validar a finalidade da coluna com o responsável de negócio antes de removê-la, ocultá-la ou modelar estruturas dependentes.",
        "evidence": evidence,
        "question": _question(profile, severity),
    }]
