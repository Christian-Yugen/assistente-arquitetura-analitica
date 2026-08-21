from __future__ import annotations

import dataclasses
import unittest

from engine.granularity.composite import CompositeGrainSheetProfile, classify_composite_grain
from engine.profiling.composite_grain import CompositeGrainAccumulator


def composite_rows() -> list[tuple[str, str]]:
    return [(f"grupo-{left}", f"codigo-{right}") for left in range(4) for right in range(5)]


class CompositeGrainTests(unittest.TestCase):
    def test_detects_jointly_unique_non_unique_components_at_minimum_base(self) -> None:
        accumulator = CompositeGrainAccumulator(((0, 1),))
        for row in composite_rows():
            accumulator.consume(row)
        profile = accumulator.finalize(eligible_pair_count=1)
        candidates = classify_composite_grain(CompositeGrainSheetProfile(profile, frozenset({0, 1})))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["grain_type"], "composite_key_candidate")
        self.assertEqual(candidates[0]["evidence"]["joint_uniqueness_ratio"], 1.0)

    def test_rejects_incomplete_pair(self) -> None:
        accumulator = CompositeGrainAccumulator(((0, 1),))
        for row in composite_rows()[:-1] + [("grupo-3", None)]:
            accumulator.consume(row)
        profile = accumulator.finalize(eligible_pair_count=1)
        self.assertEqual(classify_composite_grain(CompositeGrainSheetProfile(profile, frozenset({0, 1}))), [])

    def test_profile_does_not_retain_values_or_headers(self) -> None:
        accumulator = CompositeGrainAccumulator(((0, 1),))
        for row in composite_rows():
            accumulator.consume(row)
        serialized = str(dataclasses.asdict(accumulator.finalize(eligible_pair_count=1)))
        self.assertNotIn("grupo-0", serialized)
        self.assertNotIn("codigo-0", serialized)

