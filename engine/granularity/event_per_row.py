"""GRN-EVENT-004: hipótese privada de um evento pontual por linha."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EventPerRowSheetProfile:
    """Contagens agregadas definidas na Proposta A aprovada para a GRN-EVENT-004."""

    observed_row_count: int
    event_header_eligible_count: int
    explicit_key_candidate_count: int
    non_competence_date_candidate_count: int
    excluded_event_marker_count: int
    event_marker_formula_count: int
    ambiguity_count: int
    basis: str = "closed_event_marker_explicit_key_non_competence_date_v1"


def classify_event_per_row(profile: EventPerRowSheetProfile) -> list[dict[str, object]]:
    """Emite uma hipótese bloqueante sem identificar colunas, cabeçalhos ou valores."""

    if (
        profile.observed_row_count < 20
        or profile.event_header_eligible_count != 1
        or profile.excluded_event_marker_count != 0
        or profile.event_marker_formula_count != 0
        or profile.explicit_key_candidate_count != 1
        or profile.non_competence_date_candidate_count != 1
        or profile.ambiguity_count != 0
    ):
        return []

    return [{
        "rule_id": "GRN-EVENT-004",
        "grain_type": "event_per_row_candidate",
        "confidence": 0.80,
        "evidence": {
            "minimum_observed_row_count": 20,
            "observed_row_count": profile.observed_row_count,
            "event_header_eligible_count": profile.event_header_eligible_count,
            "explicit_key_candidate_count": profile.explicit_key_candidate_count,
            "non_competence_date_candidate_count": profile.non_competence_date_candidate_count,
            "excluded_event_marker_count": profile.excluded_event_marker_count,
            "event_marker_formula_count": profile.event_marker_formula_count,
            "ambiguity_count": profile.ambiguity_count,
            "basis": profile.basis,
        },
        "question": {
            "text": "Cada linha desta aba representa um evento pontual identificável no processo de negócio?",
            "reason": "Os sinais técnicos observados não confirmam o significado de negócio de cada linha sem validação humana.",
            "question_type": "confirmation",
            "priority": "high",
            "blocking": True,
            "options": [],
        },
    }]
