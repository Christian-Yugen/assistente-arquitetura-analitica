"""REL-ORPHAN-003: hipótese privada de referência sem cobertura integral."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrphanReferenceRelationshipPairProfile:
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
    fact_reference_complete: bool = False
    fact_reference_unique: bool = False
    referential_coverage_ratio: float = 0.0
    uncovered_reference_distinct_count: int = 0
    eligible_direction_count: int = 0
    has_one_to_one_pattern: bool = False
    has_many_to_many_pattern: bool = False
    ambiguity_count: int = 0


def classify_orphan_reference_relationship(
    profile: OrphanReferenceRelationshipPairProfile,
) -> dict[str, object] | None:
    """Emite alerta agregado; nunca identifica referências, linhas ou correções."""

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
        and profile.dimension_key_unique
        and profile.fact_reference_complete
        and not profile.fact_reference_unique
        and 0.0 < profile.referential_coverage_ratio < 1.0
        and profile.uncovered_reference_distinct_count > 0
        and profile.eligible_direction_count == 1
    )
    if blocked or not eligible:
        return None

    return {
        "rule_id": "REL-ORPHAN-003",
        "relationship_type": "orphan_reference_candidate",
        "confidence": 0.80,
        "severity": "warning",
        "evidence": {
            "source_standard_dimension_candidate": True,
            "target_fact_candidate": True,
            "eligible_dimension_key_count": 1,
            "eligible_fact_reference_count": 1,
            "dimension_key_complete": True,
            "dimension_key_unique": True,
            "fact_reference_complete": True,
            "fact_reference_unique": False,
            "referential_coverage_ratio": profile.referential_coverage_ratio,
            "uncovered_reference_distinct_count": profile.uncovered_reference_distinct_count,
            "eligible_direction_count": 1,
        },
        "question": {
            "text": "Revise a cobertura referencial parcial antes de orientar qualquer relacionamento no modelo.",
            "reason": "A regra não identifica referências sem cobertura, não confirma erro de negócio e não altera dados ou relacionamentos.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": ["Confirmar revisão", "Rejeitar alerta", "Revisar evidências"],
        },
    }
