"""REL-COMPKEY-009: hipótese privada de chave composta por dois campos."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompositeRelationshipKeyPairProfile:
    """Perfil agregado que não contém abas, colunas, valores, tuplas ou assinaturas."""

    source_standard_dimension_candidate: bool = False
    target_fact_candidate: bool = False
    source_calendar_dimension_candidate: bool = False
    source_or_target_undefined_candidate: bool = False
    source_or_target_fact_without_grain_candidate: bool = False
    source_or_target_classification_conflict: bool = False
    source_or_target_sensitive: bool = False
    source_or_target_has_formula: bool = False
    self_reference: bool = False
    eligible_composite_key_pair_count: int = 0
    eligible_composite_reference_pair_count: int = 0
    has_eligible_simple_key: bool = False
    composite_key_complete: bool = False
    composite_key_unique: bool = False
    composite_reference_complete: bool = False
    composite_reference_unique: bool = False
    referential_coverage_ratio: float = 0.0
    eligible_direction_count: int = 0
    has_one_to_one_pattern: bool = False
    has_many_to_many_pattern: bool = False
    ambiguity_count: int = 0


def classify_composite_relationship_key(profile: CompositeRelationshipKeyPairProfile) -> dict[str, object] | None:
    """Emite somente hipótese revisável e nunca cria colunas concatenadas ou relações."""

    blocked = (
        profile.source_calendar_dimension_candidate
        or profile.source_or_target_undefined_candidate
        or profile.source_or_target_fact_without_grain_candidate
        or profile.source_or_target_classification_conflict
        or profile.source_or_target_sensitive
        or profile.source_or_target_has_formula
        or profile.self_reference
        or profile.has_eligible_simple_key
        or profile.has_one_to_one_pattern
        or profile.has_many_to_many_pattern
        or profile.ambiguity_count > 0
    )
    eligible = (
        profile.source_standard_dimension_candidate
        and profile.target_fact_candidate
        and profile.eligible_composite_key_pair_count == 1
        and profile.eligible_composite_reference_pair_count == 1
        and profile.composite_key_complete
        and profile.composite_key_unique
        and profile.composite_reference_complete
        and not profile.composite_reference_unique
        and profile.referential_coverage_ratio == 1.0
        and profile.eligible_direction_count == 1
    )
    if blocked or not eligible:
        return None

    return {
        "rule_id": "REL-COMPKEY-009",
        "relationship_type": "composite_relationship_key_review_candidate",
        "confidence": 0.70,
        "severity": "review_required",
        "evidence": {
            "eligible_composite_key_pair_count": 1,
            "eligible_composite_reference_pair_count": 1,
            "has_eligible_simple_key": False,
            "composite_key_complete": True,
            "composite_key_unique": True,
            "composite_reference_complete": True,
            "composite_reference_unique": False,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": 1,
        },
        "question": {
            "text": "Revise e confirme a hipótese de chave composta por dois campos antes de orientar a modelagem.",
            "reason": "A regra não revela campos, tuplas ou valores e não cria colunas concatenadas, relações ou filtros.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": ["Confirmar chave composta", "Indicar outra chave", "Indicar que não deve haver relação"],
        },
    }
