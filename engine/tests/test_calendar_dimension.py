from __future__ import annotations

import unittest
from datetime import date, timedelta

from engine.fact_dimension.calendar_dimension import CalendarDimensionSheetProfile, classify_calendar_dimension
from engine.profiling.calendar_dimension import CalendarDateProfile, profile_calendar_date


class CalendarDimensionTests(unittest.TestCase):
    def test_profile_counts_daily_continuity_without_retaining_dates(self):
        values = [date(2025, 1, 1) + timedelta(days=index) for index in range(20)]
        profile = profile_calendar_date(values)
        self.assertEqual(profile.recognized_date_count, 20)
        self.assertEqual(profile.distinct_date_count, 20)
        self.assertEqual(profile.consecutive_day_transition_count, 19)

    def test_candidate_requires_convergent_calendar_signals(self):
        candidate = classify_calendar_dimension(CalendarDimensionSheetProfile(
            observed_row_count=20,
            grain_available=True,
            calendar_dates=(CalendarDateProfile(20, 20, 19),),
            eligible_measure_column_count=0,
        ))
        self.assertEqual(candidate[0]["classification_type"], "dimension_calendar_candidate")
        self.assertEqual(candidate[0]["confidence"], 0.75)
        self.assertEqual(candidate[0]["evidence"]["consecutive_day_transition_count"], 19)
        self.assertTrue(candidate[0]["question"]["blocking"])

    def test_insufficient_rows_do_not_classify(self):
        self.assertEqual(classify_calendar_dimension(CalendarDimensionSheetProfile(
            observed_row_count=19,
            grain_available=True,
            calendar_dates=(CalendarDateProfile(19, 19, 18),),
            eligible_measure_column_count=0,
        )), [])

    def test_missing_or_excluding_signals_do_not_classify(self):
        base = dict(
            observed_row_count=20,
            grain_available=True,
            calendar_dates=(CalendarDateProfile(20, 20, 19),),
            eligible_measure_column_count=0,
        )
        disqualifiers = (
            {"grain_available": False},
            {"calendar_dates": (CalendarDateProfile(19, 19, 18),)},
            {"calendar_dates": (CalendarDateProfile(20, 19, 18),)},
            {"calendar_dates": (CalendarDateProfile(20, 20, 18),)},
            {"eligible_measure_column_count": 1},
        )
        for update in disqualifiers:
            with self.subTest(update=update):
                self.assertEqual(classify_calendar_dimension(CalendarDimensionSheetProfile(**(base | update))), [])


if __name__ == "__main__":
    unittest.main()
