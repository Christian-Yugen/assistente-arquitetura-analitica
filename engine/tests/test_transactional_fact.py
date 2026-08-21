from __future__ import annotations

import unittest
from datetime import date

from engine.fact_dimension.transactional import TransactionalFactSheetProfile, classify_transactional_fact
from engine.profiling.transactional_fact import profile_transactional_date


class TransactionalFactTests(unittest.TestCase):
    def test_profile_counts_distinct_days_without_retaining_values(self):
        profile = profile_transactional_date([date(2025, 1, 1), "02/01/2025", "2025-01-03", "31-02-2025"])
        self.assertEqual(profile.recognized_date_count, 3)
        self.assertEqual(profile.distinct_date_count, 3)
        self.assertNotIn("2025-01", repr(profile))

    def test_candidate_requires_grain_high_variability_and_measure(self):
        dates = profile_transactional_date([date(2025, 1, day) for day in range(1, 21)])
        candidate = classify_transactional_fact(TransactionalFactSheetProfile(20, True, (dates,), 1))
        self.assertEqual(candidate[0]["classification_type"], "fact_transactional_candidate")
        self.assertEqual(candidate[0]["confidence"], 0.70)
        self.assertEqual(candidate[0]["evidence"]["temporal_distinct_ratio"], 1.0)
        self.assertTrue(candidate[0]["question"]["blocking"])

    def test_insufficient_rows_do_not_classify(self):
        dates = profile_transactional_date([date(2025, 1, day) for day in range(1, 20)])
        self.assertEqual(classify_transactional_fact(TransactionalFactSheetProfile(19, True, (dates,), 1)), [])

    def test_missing_grain_low_variability_or_measure_do_not_classify(self):
        high_variability = profile_transactional_date([date(2025, 1, day) for day in range(1, 21)])
        low_variability = profile_transactional_date([date(2025, 1, day) for day in range(1, 5)] * 5)
        self.assertEqual(classify_transactional_fact(TransactionalFactSheetProfile(20, False, (high_variability,), 1)), [])
        self.assertEqual(classify_transactional_fact(TransactionalFactSheetProfile(20, True, (low_variability,), 1)), [])
        self.assertEqual(classify_transactional_fact(TransactionalFactSheetProfile(20, True, (high_variability,), 0)), [])


if __name__ == "__main__":
    unittest.main()
