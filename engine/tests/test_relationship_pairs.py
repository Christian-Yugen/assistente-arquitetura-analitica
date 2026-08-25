import unittest

from engine.profiling.relationship_pairs import RelationshipColumnAccumulator, RelationshipPairSignal


class RelationshipPairAccumulatorTests(unittest.TestCase):
    def test_reduces_transient_signatures_to_aggregated_coverage(self):
        dimension = RelationshipColumnAccumulator()
        fact = RelationshipColumnAccumulator()
        for value in ("A", "B", "C"):
            dimension.consume(value, is_formula=False)
        for value in ("A", "A", "C", "C"):
            fact.consume(value, is_formula=False)

        self.assertTrue(dimension.complete)
        self.assertTrue(dimension.unique)
        self.assertTrue(fact.complete)
        self.assertFalse(fact.unique)
        self.assertEqual(fact.coverage_from(dimension), 1.0)

        signal = RelationshipPairSignal(
            source_sheet_id="opaque-sheet-a",
            source_column_id="opaque-column-a",
            target_sheet_id="opaque-sheet-b",
            target_column_id="opaque-column-b",
            source_observed_count=dimension.observed_count,
            source_non_missing_count=dimension.non_missing_count,
            source_distinct_count=dimension.distinct_count,
            target_observed_count=fact.observed_count,
            target_non_missing_count=fact.non_missing_count,
            target_distinct_count=fact.distinct_count,
            source_complete=dimension.complete,
            source_unique=dimension.unique,
            target_complete=fact.complete,
            target_unique=fact.unique,
            referential_coverage_ratio=fact.coverage_from(dimension),
            uncovered_reference_distinct_count=fact.uncovered_distinct_count_from(dimension),
            source_or_target_sensitive=False,
            source_or_target_has_formula=False,
        )
        prohibited = {"sheet_name", "column_name", "header", "value", "example", "frequency"}
        self.assertTrue(prohibited.isdisjoint(signal.__dataclass_fields__))

        dimension.clear()
        fact.clear()
        self.assertEqual(dimension.distinct_count, 0)
        self.assertEqual(fact.distinct_count, 0)

    def test_reduces_uncovered_references_to_a_count_without_retaining_values(self):
        dimension = RelationshipColumnAccumulator()
        fact = RelationshipColumnAccumulator()
        for value in ("A", "B", "C"):
            dimension.consume(value, is_formula=False)
        for value in ("A", "A", "UNMATCHED", "UNMATCHED"):
            fact.consume(value, is_formula=False)

        self.assertEqual(fact.coverage_from(dimension), 0.5)
        self.assertEqual(fact.uncovered_distinct_count_from(dimension), 1)
        dimension.clear()
        fact.clear()

    def test_formula_blocks_and_is_not_converted_to_a_signature(self):
        accumulator = RelationshipColumnAccumulator()
        accumulator.consume("=A2", is_formula=True)

        self.assertTrue(accumulator.has_formula)
        self.assertFalse(accumulator.complete)
        self.assertEqual(accumulator.distinct_count, 0)
