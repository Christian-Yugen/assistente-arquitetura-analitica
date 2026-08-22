from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EntityPerRowSheetProfile:
    """Contagens agregadas aprovadas para a hipótese GRN-ENTITY-003."""

    observed_row_count: int
    entity_header_eligible_count: int
    explicit_key_candidate_count: int
    descriptive_attribute_candidate_count: int
    non_competence_date_candidate_count: int
    event_candidate_count: int
    measure_candidate_count: int
    sensitive_candidate_count: int
    excluded_entity_marker_count: int
    entity_marker_formula_count: int
    ambiguity_count: int
    basis: str = "closed_entity_marker_explicit_key_descriptive_attribute_without_event_time_measure_v1"


def classify_entity_per_row(profile: EntityPerRowSheetProfile) -> list[dict[str, object]]:
    """Emite hipótese bloqueante sem identificar abas, colunas, cabeçalhos ou valores."""

    if (
        profile.observed_row_count < 20
        or profile.entity_header_eligible_count != 1
        or profile.explicit_key_candidate_count != 1
        or profile.descriptive_attribute_candidate_count < 1
        or profile.non_competence_date_candidate_count != 0
        or profile.event_candidate_count != 0
        or profile.measure_candidate_count != 0
        or profile.sensitive_candidate_count != 0
        or profile.excluded_entity_marker_count != 0
        or profile.entity_marker_formula_count != 0
        or profile.ambiguity_count != 0
    ):
        return []

    return [{
        "rule_id": "GRN-ENTITY-003",
        "grain_type": "entity_per_row_candidate",
        "confidence": 0.75,
        "evidence": {
            "minimum_observed_row_count": 20,
            "observed_row_count": profile.observed_row_count,
            "entity_header_eligible_count": profile.entity_header_eligible_count,
            "explicit_key_candidate_count": profile.explicit_key_candidate_count,
            "descriptive_attribute_candidate_count": profile.descriptive_attribute_candidate_count,
            "non_competence_date_candidate_count": profile.non_competence_date_candidate_count,
            "event_candidate_count": profile.event_candidate_count,
            "measure_candidate_count": profile.measure_candidate_count,
            "sensitive_candidate_count": profile.sensitive_candidate_count,
            "excluded_entity_marker_count": profile.excluded_entity_marker_count,
            "entity_marker_formula_count": profile.entity_marker_formula_count,
            "ambiguity_count": profile.ambiguity_count,
            "basis": profile.basis,
        },
        "question": {
            "text": "Cada linha desta aba representa uma entidade estável de cadastro, e não um evento, período, relacionamento ou medida?",
            "reason": "Os sinais técnicos observados não confirmam o significado de negócio de cada linha sem validação humana.",
            "question_type": "confirmation",
            "priority": "high",
            "blocking": True,
            "options": [],
        },
    }]
