from __future__ import annotations

import unittest

from engine.calibration.evaluate_mdl_dimcal_draft_golden import evaluate


class CalendarDimensionGoldenTests(unittest.TestCase):
    def test_golden_dataset_remains_calibrated(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})


if __name__ == "__main__":
    unittest.main()
