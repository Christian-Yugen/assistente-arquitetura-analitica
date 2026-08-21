from __future__ import annotations

import unittest
from datetime import date

from engine.fact_dimension.periodic import PeriodicFactSheetProfile, classify_periodic_fact
from engine.profiling.periodic_fact import profile_periodic_date


class PeriodicFactTests(unittest.TestCase):
    def test_period_profile_counts_months_without_retaining_values(self):
        profile = profile_periodic_date([date(2025, 1, 1), "15/01/2025", "2025-02-01", "31-02-2025"])
        self.assertEqual(profile.recognized_date_count, 3)
        self.assertEqual(profile.distinct_period_count, 2)
        self.assertNotIn("2025-01", repr(profile))

    def test_candidate_requires_grain_period_and_measure(self):
        periodic = profile_periodic_date(["2025-01-01"] * 10 + ["2025-02-01"] * 10)
        candidate = classify_periodic_fact(PeriodicFactSheetProfile(20, True, (periodic,), 1))
        self.assertEqual(candidate[0]["classification_type"], "fact_periodic_candidate")
        self.assertEqual(candidate[0]["confidence"], 0.70)
        self.assertEqual(candidate[0]["evidence"]["distinct_period_count"], 2)

    def test_insufficient_rows_or_periods_do_not_classify(self):
        one_period = profile_periodic_date(["2025-01-01"] * 20)
        self.assertEqual(classify_periodic_fact(PeriodicFactSheetProfile(20, True, (one_period,), 1)), [])
        self.assertEqual(classify_periodic_fact(PeriodicFactSheetProfile(19, True, (one_period,), 1)), [])


if __name__ == "__main__":
    unittest.main()
