import dataclasses
import unittest

from engine.profiling.relationship_pairs import CompositeRelationshipAccumulator, CompositeRelationshipPairSignal


class CompositeRelationshipProfilerTests(unittest.TestCase):
    def test_keeps_tuple_signatures_transient_and_returns_only_aggregate_metrics(self):
        source = CompositeRelationshipAccumulator()
        target = CompositeRelationshipAccumulator()
        for values in (("a", 1), ("b", 1), ("a", 2)):
            source.consume(values, has_formula=False)
        for values in (("a", 1), ("a", 1), ("b", 1), ("a", 2)):
            target.consume(values, has_formula=False)

        signal = CompositeRelationshipPairSignal(
            source_sheet_id="opaque-source",
            target_sheet_id="opaque-target",
            eligible_composite_key_pair_count=1,
            eligible_composite_reference_pair_count=1,
            composite_key_complete=source.complete,
            composite_key_unique=source.unique,
            composite_reference_complete=target.complete,
            composite_reference_unique=target.unique,
            referential_coverage_ratio=target.coverage_from(source),
            eligible_direction_count=1,
            has_one_to_one_pattern=False,
            has_many_to_many_pattern=False,
            source_or_target_sensitive=False,
            source_or_target_has_formula=False,
        )
        source.clear()
        target.clear()

        self.assertTrue(signal.composite_key_unique)
        self.assertFalse(signal.composite_reference_unique)
        self.assertEqual(signal.referential_coverage_ratio, 1.0)
        self.assertFalse(source._signatures)
        self.assertFalse(target._signatures)
        field_names = {field.name for field in dataclasses.fields(CompositeRelationshipPairSignal)}
        self.assertFalse({name for name in field_names if any(token in name for token in ("column", "value", "tuple", "signature", "header"))})
