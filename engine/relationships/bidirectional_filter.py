"""REL-BIDIR-008: hipótese privada de revisão para eventual filtro bidirecional."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BidirectionalFilterReviewPairProfile:
    """Perfil agregável de par opaco, deliberadamente sem nomes, valores ou posições."""

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
    eligible_direction_count: int = 0
    has_one_to_one_pattern: bool = False
    has_many_to_many_pattern: bool = False
    ambiguity_count: int = 0


def classify_bidirectional_filter_review(profile: BidirectionalFilterReviewPairProfile) -> dict[str, object] | None:
    """Emite somente hipótese de revisão; nunca afirma filtro existente ou cria configuração Power BI."""

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
        and profile.referential_coverage_ratio == 1.0
        and profile.eligible_direction_count == 1
    )
    if blocked or not eligible:
        return None

    return {
        "rule_id": "REL-BIDIR-008",
        "relationship_type": "bidirectional_filter_review_candidate",
        "confidence": 0.70,
        "severity": "review_required",
        "evidence": {
            "source_standard_dimension_candidate": True,
            "target_fact_candidate": True,
            "eligible_dimension_key_count": 1,
            "eligible_fact_reference_count": 1,
            "dimension_key_complete": True,
            "dimension_key_unique": True,
            "fact_reference_complete": True,
            "fact_reference_unique": False,
            "referential_coverage_ratio": 1.0,
            "eligible_direction_count": 1,
        },
        "question": {
            "text": "Se for considerada uma direção bidirecional, justifique e revise a exceção antes de orientar a modelagem.",
            "reason": "A regra não detecta filtro Power BI existente e não recomenda criar relação, filtro ou direção bidirecional.",
            "question_type": "single_choice",
            "priority": "high",
            "blocking": True,
            "options": ["Preservar direção unidirecional", "Justificar exceção bidirecional", "Indicar que não deve haver relação"],
        },
    }
