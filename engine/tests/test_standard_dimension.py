from __future__ import annotations

import unittest

from engine.fact_dimension.standard_dimension import StandardDimensionSheetProfile, classify_standard_dimension


class StandardDimensionTests(unittest.TestCase):
    def test_candidate_requires_convergent_dimension_signals(self):
        candidate = classify_standard_dimension(StandardDimensionSheetProfile(
            observed_row_count=20,
            grain_available=True,
            individually_unique_identifier_count=1,
            descriptive_attribute_count=1,
            eligible_measure_column_count=0,
            fully_recognized_temporal_column_count=0,
        ))
        self.assertEqual(candidate[0]["classification_type"], "dimension_standard_candidate")
        self.assertEqual(candidate[0]["confidence"], 0.70)
        self.assertEqual(candidate[0]["evidence"]["individually_unique_identifier_count"], 1)
        self.assertTrue(candidate[0]["question"]["blocking"])

    def test_insufficient_rows_do_not_classify(self):
        self.assertEqual(classify_standard_dimension(StandardDimensionSheetProfile(
            observed_row_count=19,
            grain_available=True,
            individually_unique_identifier_count=1,
            descriptive_attribute_count=1,
            eligible_measure_column_count=0,
            fully_recognized_temporal_column_count=0,
        )), [])

    def test_missing_or_excluding_signals_do_not_classify(self):
        base = dict(
            observed_row_count=20,
            grain_available=True,
            individually_unique_identifier_count=1,
            descriptive_attribute_count=1,
            eligible_measure_column_count=0,
            fully_recognized_temporal_column_count=0,
        )
        disqualifiers = (
            {"grain_available": False},
            {"individually_unique_identifier_count": 0},
            {"descriptive_attribute_count": 0},
            {"eligible_measure_column_count": 1},
            {"fully_recognized_temporal_column_count": 1},
        )
        for update in disqualifiers:
            with self.subTest(update=update):
                self.assertEqual(classify_standard_dimension(StandardDimensionSheetProfile(**(base | update))), [])


if __name__ == "__main__":
    unittest.main()
