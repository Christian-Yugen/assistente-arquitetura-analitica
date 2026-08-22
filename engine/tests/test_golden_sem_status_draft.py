import unittest

from engine.calibration.evaluate_sem_status_draft_golden import evaluate


class SemanticStatusGoldenTests(unittest.TestCase):
    def test_calibration_is_reproducible(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
