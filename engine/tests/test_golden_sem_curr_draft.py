import unittest

from engine.calibration.evaluate_sem_curr_draft_golden import evaluate


class SemanticCurrencyGoldenTests(unittest.TestCase):
    def test_golden_calibration(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
