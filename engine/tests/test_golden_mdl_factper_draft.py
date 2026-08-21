from __future__ import annotations

import unittest

from engine.calibration.evaluate_mdl_factper_draft_golden import evaluate


class GoldenMdlFactperTests(unittest.TestCase):
    def test_calibration_has_no_false_positives_or_false_negatives(self):
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
