"""REL-FACTFACT-006: hipótese privada de revisão de vínculo direto entre fatos."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DirectFactRelationshipPairProfile:
    """Perfil agregável de par opaco, deliberadamente sem nomes, valores ou posições."""

    source_fact_candidate: bool = False
    target_fact_candidate: bool = False
    source_or_target_dimension_candidate: bool = False
    source_or_target_undefined_candidate: bool = False
    source_or_target_fact_without_grain_candidate: bool = False
    source_or_target_classification_conflict: bool = False
    source_or_target_sensitive: bool = False
    source_or_target_has_formula: bool = False
    self_reference: bool = False
    eligible_source_key_count: int = 0
    eligible_target_reference_count: int = 0
    source_key_complete: bool = False
    source_key_unique: bool = False
    target_reference_complete: bool = False
    target_reference_unique: bool = False
    referential_coverage_ratio: float = 0.0
    eligible_direction_count: int = 0
    has_one_to_one_pattern: bool = False
    has_many_to_many_pattern: bool = False
    ambiguity_count: int = 0


def classify_direct_fact_relationship(profile: DirectFactRelationshipPairProfile) -> dict[str, object] | None:
    """Emite somente hipótese de revisão; nunca recomenda criar relação, ponte ou filtro."""

    blocked = (
        profile.source_or_target_dimension_candidate
        or profile.source_or_target_undefined_candidate
        or profile.source_or_target_fact_without_grain_candidate
        or profile.source_or_target_classification_conflict
        or profile.source_or_target_sensitive
        or profile.source_or_target_has_formula
        or profile.self_reference
        or profile.has_one_to_one_pattern
        or profile.has_many_to_many_pattern
        or profile.ambiguity_count > 0
    )
    eligible = (
        profile.source_fact_candidate
        and profile.target_fact_candidate
        and profile.eligible_source_key_count == 1
        and profile.eligible_target_reference_count == 1
        and profile.source_key_complete
        and profile.source_key_unique
        and profile.target_reference_complete
        and not profile.target_reference_unique
        and profile.referential_coverage_ratio == 1.0
        and profile.eligible_direction_count == 1
    )
    if blocked or not eligible:
        return None

    return {
        "rule_id": "REL-FACTFACT-006",
        "relationship_type": "direct_fact_to_fact_relationship_review_candidate",
        "confidence": 0.65,
        "severity": "review_required",
        "evidence": {
            "source_fact_candidate": True,
            "target_fact_candidate": True,
            "eligible_source_key_count": 1,
            "eligible_target_reference_count": 1,
            "source_key_complete": True,
            "source_key_unique": True,
            "target_reference_complete": True,
            "target_reference_unique": False,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": 1,
        },
        "question": {
            "text": "Revise a hipótese agregada de vínculo direto entre fatos antes de orientar a modelagem.",
            "reason": "A regra não recomenda criar relação direta, dimensão compartilhada, tabela ponte ou direção de filtro.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": ["Confirmar revisão", "Rejeitar hipótese", "Revisar dimensão compartilhada"],
        },
    }
