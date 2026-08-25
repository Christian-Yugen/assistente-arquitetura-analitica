"""REL-AMBIG-007: hipótese privada de direções candidatas concorrentes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AmbiguousRelationshipPathPairProfile:
    """Perfil agregável de par opaco, deliberadamente sem nomes, valores ou posições."""

    source_standard_dimension_candidate: bool = False
    target_fact_candidate: bool = False
    source_or_target_calendar_dimension_candidate: bool = False
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


def classify_ambiguous_relationship_path(profile: AmbiguousRelationshipPathPairProfile) -> dict[str, object] | None:
    """Emite apenas hipótese de revisão; nunca infere um caminho Power BI existente ou cria filtros."""

    blocked = (
        profile.source_or_target_calendar_dimension_candidate
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
        and profile.eligible_source_key_count >= 1
        and profile.eligible_target_reference_count >= 1
        and profile.source_key_complete
        and profile.source_key_unique
        and profile.target_reference_complete
        and not profile.target_reference_unique
        and profile.referential_coverage_ratio == 1.0
        and profile.eligible_direction_count >= 2
    )
    if blocked or not eligible:
        return None

    return {
        "rule_id": "REL-AMBIG-007",
        "relationship_type": "ambiguous_relationship_path_review_candidate",
        "confidence": 0.60,
        "severity": "review_required",
        "evidence": {
            "source_standard_dimension_candidate": True,
            "target_fact_candidate": True,
            "eligible_source_key_count": profile.eligible_source_key_count,
            "eligible_target_reference_count": profile.eligible_target_reference_count,
            "source_key_complete": True,
            "source_key_unique": True,
            "target_reference_complete": True,
            "target_reference_unique": False,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": profile.eligible_direction_count,
        },
        "question": {
            "text": "Revise as direções candidatas concorrentes antes de orientar a modelagem.",
            "reason": "A regra não confirma caminho ambíguo em Power BI e não recomenda criar relação, filtro ou direção de filtro.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": ["Confirmar revisão", "Selecionar uma direção", "Indicar que não deve haver relação"],
        },
    }
