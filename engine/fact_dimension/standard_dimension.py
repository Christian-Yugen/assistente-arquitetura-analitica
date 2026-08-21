"""MDL-DIMSTD-004: hipótese conservadora de dimensão cadastral."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StandardDimensionSheetProfile:
    observed_row_count: int
    grain_available: bool
    individually_unique_identifier_count: int
    descriptive_attribute_count: int
    eligible_measure_column_count: int
    fully_recognized_temporal_column_count: int


def classify_standard_dimension(profile: StandardDimensionSheetProfile) -> list[dict[str, object]]:
    if (
        not profile.grain_available
        or profile.observed_row_count < 20
        or profile.individually_unique_identifier_count < 1
        or profile.descriptive_attribute_count < 1
        or profile.eligible_measure_column_count > 0
        or profile.fully_recognized_temporal_column_count > 0
    ):
        return []
    return [{
        "rule_id": "MDL-DIMSTD-004",
        "classification_type": "dimension_standard_candidate",
        "confidence": 0.70,
        "evidence": {
            "observed_row_count": profile.observed_row_count,
            "individually_unique_identifier_count": profile.individually_unique_identifier_count,
            "descriptive_attribute_count": profile.descriptive_attribute_count,
            "eligible_measure_column_count": profile.eligible_measure_column_count,
            "fully_recognized_temporal_column_count": profile.fully_recognized_temporal_column_count,
            "grain_available": True,
            "basis": "grain_unique_identifier_descriptive_text_no_measure_no_temporal_min20_private_v1",
        },
        "question": {
            "text": "Confirme se cada linha representa uma entidade relativamente estável, identificada por uma chave e descrita por atributos, sem registrar medidas ou eventos.",
            "reason": "Chave individualmente única, atributos descritivos e ausência de medidas ou tempo sugerem dimensão cadastral, mas a semântica de negócio exige validação humana.",
            "question_type": "confirmation", "priority": "high", "blocking": True, "options": [],
        },
    }]
