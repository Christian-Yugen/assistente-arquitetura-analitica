import unittest

from engine.calibration.evaluate_sem_qty_draft_golden import evaluate


class SemanticQuantityGoldenTests(unittest.TestCase):
    def test_golden_calibration(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
