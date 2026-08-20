"""QLT-MIXTYPE-005: coexistência conservadora de tipos físicos incompatíveis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.mixed_types import MixedTypesProfile, NORMALIZATION_BASIS


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class MixedTypesColumnProfile:
    """O nome é recebido apenas para compatibilidade de contexto e nunca é emitido."""

    name: str
    mixed_types: MixedTypesProfile


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


def _eligible_groups(profile: MixedTypesProfile) -> tuple[tuple[str, int], ...]:
    return tuple((group, count) for group, count in profile.group_counts() if count >= 2)


def _is_consistent(profile: MixedTypesProfile) -> bool:
    observed = sum(count for _, count in profile.group_counts()) + profile.strict_numeric_text_count + profile.unsupported_count
    return observed == profile.non_empty_value_count and all(count >= 0 for _, count in profile.group_counts())


def _is_applicable(profile: MixedTypesProfile) -> bool:
    return (
        profile.normalization_basis == NORMALIZATION_BASIS
        and profile.non_empty_value_count >= 5
        and _is_consistent(profile)
        and len(_eligible_groups(profile)) >= 2
    )


def _severity(minority_ratio: float) -> Severity:
    if minority_ratio < 0.10:
        return "low"
    if minority_ratio < 0.30:
        return "medium"
    return "high"


def _question(severity: Severity) -> dict[str, object] | None:
    if severity == "low":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": severity == "high",
        "text": "A coluna reúne grupos físicos de dados potencialmente incompatíveis. Eles representam significados distintos ou uma inconsistência de origem?",
        "reason": "A confirmação evita conversão ou exclusão indevida antes de compreender a semântica de negócio.",
        "options": [
            {"option_id": "distinct_meanings", "label": "Representam significados distintos e devem ser separados ou tratados explicitamente."},
            {"option_id": "source_inconsistency", "label": "Representam uma inconsistência e devem ser corrigidos na origem após validação."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_mixed_types(profile: MixedTypesColumnProfile) -> list[Finding]:
    """Emite no máximo um finding agregado, sem valores, posições ou nomes de coluna."""

    mixed_types = profile.mixed_types
    if not _is_applicable(mixed_types):
        return []
    eligible_groups = _eligible_groups(mixed_types)
    minority_count = min(count for _, count in eligible_groups)
    minority_ratio = round(minority_count / mixed_types.non_empty_value_count, 8)
    severity = _severity(minority_ratio)
    group_codes = ",".join(group for group, _ in eligible_groups)
    evidence: list[dict[str, object]] = [
        {"code": "EVD-MIXTYPE-NONEMPTY", "effect": "technical", "observed_value": mixed_types.non_empty_value_count, "expected_condition": "non_empty_value_count >= 5"},
        {"code": "EVD-MIXTYPE-GROUPS", "effect": "negative", "observed_value": len(eligible_groups), "expected_condition": "eligible_physical_group_count >= 2"},
        {"code": "EVD-MIXTYPE-MINORITY-RATIO", "effect": "negative", "observed_ratio": minority_ratio, "expected_condition": "each_eligible_group_count >= 2"},
        {"code": "EVD-MIXTYPE-NORMALIZATION", "effect": "technical", "observed_value": mixed_types.normalization_basis, "expected_condition": NORMALIZATION_BASIS},
    ]
    for group, count in eligible_groups:
        evidence.append({"code": f"EVD-MIXTYPE-{group.upper()}", "effect": "technical", "observed_value": count, "expected_condition": f"{group}_count >= 2"})
    return [{
        "rule_id": "QLT-MIXTYPE-005",
        "category": "quality",
        "severity": severity,
        "confidence": 0.95,
        "title": "Coexistência de tipos físicos incompatíveis",
        "description": f"Foram identificados {len(eligible_groups)} grupos físicos incompatíveis na região observada ({group_codes}), sem expor valores ou identificadores da coluna.",
        "impact": "A coexistência pode comprometer validações, classificação semântica e preparação analítica se não for confirmada na origem.",
        "recommendation": "Validar a semântica dos grupos com o responsável de negócio antes de qualquer conversão, exclusão ou separação na origem.",
        "evidence": evidence,
        "question": _question(severity),
    }]
