import unittest

from engine.calibration.evaluate_sem_id_draft_golden import evaluate


class GoldenSemanticIdentifierTests(unittest.TestCase):
    def test_calibration_has_no_false_positive_or_negative(self):
        self.assertEqual(evaluate(), {"tp": 2, "fp": 0, "fn": 0})
