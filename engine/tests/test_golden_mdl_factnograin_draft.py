from __future__ import annotations

import unittest

from engine.calibration.evaluate_mdl_factnograin_draft_golden import evaluate


class GoldenMdlFactWithoutGrainTests(unittest.TestCase):
    def test_calibration_has_no_false_positives_or_false_negatives(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
