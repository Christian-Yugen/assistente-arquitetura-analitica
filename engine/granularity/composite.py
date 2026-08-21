"""GRN-COMP-001: hipótese conservadora de chave composta por aba."""

from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.composite_grain import CompositeGrainProfile


@dataclass(frozen=True)
class CompositeGrainSheetProfile:
    composite_grain: CompositeGrainProfile
    semantic_identifier_component_positions: frozenset[int]


def classify_composite_grain(profile: CompositeGrainSheetProfile) -> list[dict[str, object]]:
    for pair in profile.composite_grain.pairs:
        positions = {pair.left_position, pair.right_position}
        if (
            not positions.issubset(profile.semantic_identifier_component_positions)
            or pair.observed_row_count < 20
            or pair.complete_pair_row_count != pair.observed_row_count
            or pair.left_distinct_count == pair.observed_row_count
            or pair.right_distinct_count == pair.observed_row_count
            or pair.joint_uniqueness_ratio != 1.0
        ):
            continue
        return [{
            "rule_id": "GRN-COMP-001",
            "grain_type": "composite_key_candidate",
            "confidence": 0.70,
            "evidence": {
                "observed_row_count": pair.observed_row_count,
                "complete_pair_row_count": pair.complete_pair_row_count,
                "joint_distinct_count": pair.joint_distinct_count,
                "joint_uniqueness_ratio": pair.joint_uniqueness_ratio,
                "eligible_pair_count": profile.composite_grain.eligible_pair_count,
                "examined_pair_count": profile.composite_grain.examined_pair_count,
                "component_count": 2,
                "basis": profile.composite_grain.basis,
            },
            "question": {
                "text": "Confirme se a combinação de dois componentes identificadores representa o grão desta aba.",
                "reason": "A unicidade conjunta observada é uma hipótese técnica e não confirma a definição de negócio sem validação humana.",
                "question_type": "confirmation", "priority": "high", "blocking": True, "options": [],
            },
        }]
    return []
