"""REL-NONUNIQ-002: alerta privado de chave não única no lado 1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NonUniqueOneSideRelationshipPairProfile:
    """Perfil persistível de um par opaco, sem nomes, valores ou identificadores."""

    source_standard_dimension_candidate: bool = False
    target_fact_candidate: bool = False
    source_calendar_dimension_candidate: bool = False
    source_or_target_undefined_candidate: bool = False
    source_or_target_fact_without_grain_candidate: bool = False
    source_or_target_classification_conflict: bool = False
    source_or_target_sensitive: bool = False
    source_or_target_has_formula: bool = False
    self_reference: bool = False
    eligible_dimension_key_count: int = 0
    eligible_fact_reference_count: int = 0
    dimension_key_complete: bool = False
    dimension_key_unique: bool = False
    dimension_key_duplicate_count: int = 0
    fact_reference_complete: bool = False
    referential_coverage_ratio: float = 0.0
    eligible_direction_count: int = 0
    has_one_to_one_pattern: bool = False
    has_many_to_many_pattern: bool = False
    ambiguity_count: int = 0


def classify_non_unique_one_side_relationship(
    profile: NonUniqueOneSideRelationshipPairProfile,
) -> dict[str, object] | None:
    """Emite alerta agregado; nunca identifica a chave ou corrige registros."""

    blocked = (
        profile.source_calendar_dimension_candidate
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
        profile.source_standard_dimension_candidate
        and profile.target_fact_candidate
        and profile.eligible_dimension_key_count == 1
        and profile.eligible_fact_reference_count == 1
        and profile.dimension_key_complete
        and not profile.dimension_key_unique
        and profile.dimension_key_duplicate_count > 0
        and profile.fact_reference_complete
        and profile.referential_coverage_ratio == 1.0
        and profile.eligible_direction_count == 1
    )
    if blocked or not eligible:
        return None

    return {
        "rule_id": "REL-NONUNIQ-002",
        "relationship_type": "one_side_key_non_unique_candidate",
        "confidence": 0.80,
        "severity": "warning",
        "evidence": {
            "source_standard_dimension_candidate": True,
            "target_fact_candidate": True,
            "eligible_dimension_key_count": 1,
            "eligible_fact_reference_count": 1,
            "dimension_key_complete": True,
            "dimension_key_unique": False,
            "dimension_key_duplicate_count": profile.dimension_key_duplicate_count,
            "fact_reference_complete": True,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": 1,
        },
        "question": {
            "text": "Revise a unicidade agregada do lado 1 antes de orientar qualquer relacionamento no modelo.",
            "reason": "A regra não identifica valores duplicados, não confirma chave e não altera dados ou relacionamentos.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": ["Confirmar revisão", "Rejeitar alerta", "Revisar evidências"],
        },
    }
