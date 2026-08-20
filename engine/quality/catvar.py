"""QLT-CATVAR-008: revela variações técnicas de grafia sem fundir categorias."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.categorical_variations import CategoricalVariationProfile, NORMALIZATION_BASIS


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class CategoricalVariationColumnProfile:
    name: str
    physical_type: str
    variations: CategoricalVariationProfile


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


def _is_applicable(profile: CategoricalVariationColumnProfile) -> bool:
    variations = profile.variations
    return (
        profile.physical_type in {"text", "mixed"}
        and variations.text_value_count >= 2
        and variations.distinct_text_count >= 2
        and not variations.high_cardinality
        and variations.collision_group_count > 0
        and variations.affected_value_count > 0
        and variations.affected_value_ratio > 0
        and variations.normalization_basis == NORMALIZATION_BASIS
        and variations.dictionary_entry_count == 0
    )


def _severity(ratio: float) -> Severity:
    if ratio < 0.05:
        return "low"
    if ratio < 0.2:
        return "medium"
    return "high"


def _confidence(profile: CategoricalVariationColumnProfile) -> float:
    variants = profile.variations.max_variants_in_group
    distinct = profile.variations.distinct_text_count
    penalty = 0.18 if variants > 3 else 0.0
    penalty = max(penalty, 0.18 if distinct > 50 else 0.0)
    return round(max(0.5, 0.88 - penalty), 2)


def _question(profile: CategoricalVariationColumnProfile, severity: Severity) -> dict[str, object] | None:
    if severity != "high":
        return None
    return {
        "question_type": "single_choice",
        "priority": "high",
        "blocking": True,
        "text": (
            f"A coluna {profile.name} possui grafias tecnicamente similares em parcela relevante dos registros. "
            "Elas representam a mesma categoria de negócio?"
        ),
        "reason": "A confirmação define se uma futura padronização pode ocorrer na fonte ou em uma dimensão controlada.",
        "options": [
            {"option_id": "same_category", "label": "Representam a mesma categoria e devem ser padronizadas com regra aprovada."},
            {"option_id": "different_categories", "label": "Representam categorias distintas e devem permanecer separadas."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "classification", "report"],
    }


def evaluate_categorical_variations(profile: CategoricalVariationColumnProfile) -> list[Finding]:
    """Emite candidato agregado; não revela grafias e não altera categorias."""

    if not _is_applicable(profile):
        return []
    variations = profile.variations
    severity = _severity(variations.affected_value_ratio)
    severity_copy = {
        "low": ("Poucas variações técnicas de categoria", "A padronização pode afetar filtros e agrupamentos pontuais."),
        "medium": ("Variações relevantes de categoria", "Agrupamentos, filtros e dimensões categóricas podem fragmentar resultados."),
        "high": ("Variações frequentes de categoria", "A confirmação de negócio é necessária antes de qualquer padronização ou modelagem dependente."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-CATVAR-GROUPS", "effect": "negative", "observed_value": variations.collision_group_count, "expected_condition": "collision_group_count = 0"},
        {"code": "EVD-CATVAR-AFFECTED-COUNT", "effect": "negative", "observed_value": variations.affected_value_count, "expected_condition": "affected_value_count = 0"},
        {"code": "EVD-CATVAR-AFFECTED-RATIO", "effect": "negative", "observed_value": variations.affected_value_ratio, "expected_condition": "affected_value_ratio = 0"},
        {"code": "EVD-CATVAR-NORMALIZATION", "effect": "technical", "observed_value": variations.normalization_basis, "expected_condition": NORMALIZATION_BASIS},
        {"code": "EVD-CATVAR-DICTIONARY", "effect": "governance", "observed_value": variations.dictionary_status, "expected_condition": "empty_pending_domain_approval"},
    ]
    return [{
        "rule_id": "QLT-CATVAR-008",
        "category": "quality",
        "severity": severity,
        "confidence": _confidence(profile),
        "title": severity_copy[0],
        "description": (
            f"A coluna {profile.name} possui {variations.collision_group_count} grupos de grafias tecnicamente "
            f"similares, afetando {variations.affected_value_count} valores ({variations.affected_value_ratio * 100:.1f}%)."
        ),
        "impact": severity_copy[1],
        "recommendation": "Validar se as grafias tecnicamente similares representam a mesma categoria de negócio e, se confirmado, definir uma padronização na fonte ou dimensão controlada.",
        "evidence": evidence,
        "question": _question(profile, severity),
    }]
