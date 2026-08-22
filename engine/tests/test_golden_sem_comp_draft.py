import unittest

from engine.calibration.evaluate_sem_comp_draft_golden import evaluate


class SemCompGoldenTests(unittest.TestCase):
    def test_golden_dataset_is_calibrated_without_false_results(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
