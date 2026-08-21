from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.headers import HEADERS_BASIS, HeadersProfile


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class HeadersSheetProfile:
    name: str
    headers: HeadersProfile


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


def _is_applicable(profile: HeadersSheetProfile) -> bool:
    headers = profile.headers
    if headers.basis != HEADERS_BASIS or headers.header_column_count <= 0:
        return False
    if min(headers.missing_header_count, headers.duplicate_normalized_group_count, headers.duplicate_header_count, headers.multilevel_candidate_count) < 0:
        return False
    if headers.duplicate_header_count < headers.duplicate_normalized_group_count * 2:
        return False
    return any((headers.missing_header_count, headers.duplicate_normalized_group_count, headers.multilevel_candidate_count))


def _severity(profile: HeadersProfile) -> Severity:
    if profile.multilevel_candidate_count > 0:
        return "high"
    return "medium"


def _question(severity: Severity) -> dict[str, object]:
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": severity == "high",
        "text": "A primeira linha representa o cabeçalho analítico correto e as ausências, duplicidades ou possíveis níveis adicionais são intencionais?",
        "reason": "Os sinais estruturais são determinísticos, mas a organização pretendida da aba exige confirmação humana antes de qualquer modelagem ou alteração.",
        "options": [
            {"option_id": "confirm_structure", "label": "A estrutura é intencional e deve ser mantida."},
            {"option_id": "review_headers", "label": "Os cabeçalhos precisam de revisão na origem."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_headers(profile: HeadersSheetProfile) -> list[Finding]:
    """Emite um finding por aba sem revelar cabeçalhos, títulos, posições ou ranges."""

    if not _is_applicable(profile):
        return []
    headers = profile.headers
    severity = _severity(headers)
    copy = {
        "medium": ("Estrutura de cabeçalho para validação", "Ausências ou duplicidades de cabeçalho podem dificultar a interpretação consistente das colunas."),
        "high": ("Possível cabeçalho multinível para validação", "Uma estrutura de cabeçalho em mais de um nível deve ser confirmada antes de tratar a primeira linha como esquema analítico definitivo."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-HEADERS-MISSING-COUNT", "effect": "negative", "observed_value": headers.missing_header_count, "expected_condition": "missing_header_count = 0"},
        {"code": "EVD-HEADERS-DUPLICATE-GROUPS", "effect": "negative", "observed_value": headers.duplicate_normalized_group_count, "expected_condition": "duplicate_normalized_group_count = 0"},
        {"code": "EVD-HEADERS-DUPLICATE-COUNT", "effect": "negative", "observed_value": headers.duplicate_header_count, "expected_condition": "duplicate_header_count = 0"},
        {"code": "EVD-HEADERS-MULTILEVEL-CANDIDATES", "effect": "negative", "observed_value": headers.multilevel_candidate_count, "expected_condition": "multilevel_candidate_count = 0"},
        {"code": "EVD-HEADERS-COLUMN-COUNT", "effect": "technical", "observed_value": headers.header_column_count, "expected_condition": "header_column_count > 0"},
        {"code": "EVD-HEADERS-BASIS", "effect": "technical", "observed_value": headers.basis, "expected_condition": HEADERS_BASIS},
    ]
    return [{
        "rule_id": "QLT-HEADERS-014",
        "category": "quality",
        "severity": severity,
        "confidence": 0.85,
        "title": copy[0],
        "description": "Foram identificados sinais estruturais de cabeçalho que exigem validação humana antes de qualquer interpretação analítica.",
        "impact": copy[1],
        "recommendation": "Confirmar a linha de cabeçalho e a intenção das ausências, duplicidades ou possíveis níveis adicionais diretamente na origem, sem alterar esta planilha automaticamente.",
        "evidence": evidence,
        "question": _question(severity),
    }]
