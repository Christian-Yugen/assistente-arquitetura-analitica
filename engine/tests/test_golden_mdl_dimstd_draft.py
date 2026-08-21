from __future__ import annotations

import unittest

from engine.calibration.evaluate_mdl_dimstd_draft_golden import evaluate


class GoldenMdlDimstdTests(unittest.TestCase):
    def test_calibration_has_no_false_positives_or_false_negatives(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
