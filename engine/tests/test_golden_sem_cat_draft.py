import unittest

from engine.calibration.evaluate_sem_cat_draft_golden import evaluate


class GoldenSemanticCategoryTests(unittest.TestCase):
    def test_calibration_dataset_remains_perfectly_classified(self):
        self.assertEqual(evaluate(), {"tp": 3, "fp": 0, "fn": 0})
