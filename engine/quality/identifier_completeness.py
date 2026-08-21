"""QLT-IDMISS-015: sinaliza ausência e repetição exata em identificadores elegíveis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.identifier_completeness import IdentifierCompletenessProfile, NORMALIZATION_BASIS


Severity = Literal["low", "medium", "high"]
MINIMUM_OBSERVED_CELL_COUNT = 10


@dataclass(frozen=True)
class IdentifierCompletenessColumnProfile:
    name: str
    identifiers: IdentifierCompletenessProfile


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


def _is_applicable(profile: IdentifierCompletenessColumnProfile) -> bool:
    identifiers = profile.identifiers
    if (
        not identifiers.header_eligible
        or identifiers.basis != NORMALIZATION_BASIS
        or identifiers.observed_cell_count < MINIMUM_OBSERVED_CELL_COUNT
        or identifiers.missing_cell_count < 0
        or identifiers.non_missing_cell_count < 0
        or identifiers.missing_cell_count + identifiers.non_missing_cell_count != identifiers.observed_cell_count
        or identifiers.duplicate_group_count < 0
        or identifiers.duplicate_occurrence_count < 0
        or identifiers.duplicate_occurrence_count > identifiers.non_missing_cell_count
        or identifiers.duplicate_group_count * 2 > identifiers.duplicate_occurrence_count
    ):
        return False
    expected_missing_ratio = round(identifiers.missing_cell_count / identifiers.observed_cell_count, 8)
    expected_duplicate_ratio = round(identifiers.duplicate_occurrence_count / identifiers.observed_cell_count, 8)
    return (
        identifiers.missing_ratio == expected_missing_ratio
        and identifiers.duplicate_ratio == expected_duplicate_ratio
        and (identifiers.missing_cell_count > 0 or identifiers.duplicate_occurrence_count > 0)
    )


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
        "text": "Este campo representa um identificador que deve estar completo e ser único? Há exceções de negócio para ausências ou repetições?",
        "reason": "As contagens são determinísticas, mas o vocabulário do cabeçalho não prova que a coluna seja uma chave de negócio única.",
        "options": [
            {"option_id": "unique_identifier", "label": "É um identificador que deve ser completo e único."},
            {"option_id": "valid_exception", "label": "Há exceções de negócio válidas para ausências ou repetições."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "relationships", "metrics", "report"],
    }


def evaluate_identifier_completeness(profile: IdentifierCompletenessColumnProfile) -> list[Finding]:
    """Emite hipótese agregada; não infere chave nem corrige valores ou formatos."""

    if not _is_applicable(profile):
        return []
    identifiers = profile.identifiers
    dominant_ratio = max(identifiers.missing_ratio, identifiers.duplicate_ratio)
    severity = _severity(dominant_ratio)
    severity_copy = {
        "low": ("Sinal pontual de identificador incompleto", "Uma ausência ou repetição pode comprometer a identificação de registros se o campo for uma chave de negócio."),
        "medium": ("Sinais de identificador incompleto", "A recorrência de ausências ou repetições pode prejudicar chaves, relacionamentos e validações."),
        "high": ("Muitos sinais de identificador incompleto", "A coluna deve ser validada antes de sustentar relacionamentos, contagens distintas ou recomendações analíticas."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-IDMISS-MISSING-COUNT", "effect": "negative", "observed_value": identifiers.missing_cell_count, "expected_condition": "missing_cell_count = 0"},
        {"code": "EVD-IDMISS-DUPLICATE-OCCURRENCE-COUNT", "effect": "negative", "observed_value": identifiers.duplicate_occurrence_count, "expected_condition": "duplicate_occurrence_count = 0"},
        {"code": "EVD-IDMISS-MISSING-RATIO", "effect": "negative", "observed_ratio": identifiers.missing_ratio, "expected_condition": "missing_ratio = 0"},
        {"code": "EVD-IDMISS-DUPLICATE-RATIO", "effect": "negative", "observed_ratio": identifiers.duplicate_ratio, "expected_condition": "duplicate_ratio = 0"},
        {"code": "EVD-IDMISS-OBSERVED-BASE", "effect": "technical", "observed_value": identifiers.observed_cell_count, "expected_condition": "observed_cell_count >= 10"},
        {"code": "EVD-IDMISS-BASIS", "effect": "technical", "observed_value": identifiers.basis, "expected_condition": NORMALIZATION_BASIS},
    ]
    return [{
        "rule_id": "QLT-IDMISS-015",
        "category": "quality",
        "severity": severity,
        "confidence": 0.85,
        "title": severity_copy[0],
        "description": f"Foram identificadas {identifiers.missing_cell_count} ausências e {identifiers.duplicate_occurrence_count} ocorrências duplicadas na base elegível.",
        "impact": severity_copy[1],
        "recommendation": "Confirmar com o responsável de negócio se o campo deve ser completo e único antes de definir chaves, relacionamentos, contagens distintas ou qualquer correção fora desta análise.",
        "evidence": evidence,
        "question": _question(severity),
    }]
