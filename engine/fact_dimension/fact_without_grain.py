"""MDL-FACTNOGRAIN-019: hipótese conservadora de fato sem granularidade definida."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactWithoutDefinedGrainSheetProfile:
    """Sinais exclusivamente agregados e privados para uma aba candidata."""

    observed_row_count: int
    eligible_numeric_measure_count: int
    fact_signal_count: int
    active_grain_hypothesis_count: int
    dimensional_candidate_count: int
    formula_column_count: int
    sensitive_candidate_count: int
    incompatible_temporal_signal_count: int
    ambiguity_count: int


def classify_fact_without_defined_grain(
    profile: FactWithoutDefinedGrainSheetProfile,
) -> list[dict[str, object]]:
    """Emite somente uma hipótese draft quando não há granularidade elegível."""

    if (
        profile.observed_row_count < 20
        or profile.eligible_numeric_measure_count < 1
        or profile.fact_signal_count < 1
        or profile.active_grain_hypothesis_count != 0
        or profile.dimensional_candidate_count != 0
        or profile.formula_column_count != 0
        or profile.sensitive_candidate_count != 0
        or profile.incompatible_temporal_signal_count != 0
        or profile.ambiguity_count != 0
    ):
        return []

    return [{
        "rule_id": "MDL-FACTNOGRAIN-019",
        "classification_type": "fact_without_defined_grain_candidate",
        "confidence": 0.75,
        "evidence": {
            "observed_row_count": profile.observed_row_count,
            "eligible_numeric_measure_count": profile.eligible_numeric_measure_count,
            "fact_signal_count": profile.fact_signal_count,
            "active_grain_hypothesis_count": profile.active_grain_hypothesis_count,
            "dimensional_candidate_count": profile.dimensional_candidate_count,
            "formula_column_count": profile.formula_column_count,
            "sensitive_candidate_count": profile.sensitive_candidate_count,
            "incompatible_temporal_signal_count": profile.incompatible_temporal_signal_count,
            "ambiguity_count": profile.ambiguity_count,
            "basis": "numeric_fact_signals_without_grain_min20_private_v1",
        },
        "question": {
            "text": "Confirme o que cada linha representa antes de classificar esta tabela como fato.",
            "reason": "Há medidas e sinais de fato, mas não existe hipótese de granularidade elegível; a definição do grão exige validação humana.",
            "question_type": "confirmation",
            "priority": "high",
            "blocking": True,
            "options": [],
        },
    }]
