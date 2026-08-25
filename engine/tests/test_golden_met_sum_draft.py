import hashlib
import json
import unittest
from pathlib import Path
from engine.calibration.evaluate_met_sum_draft_golden import evaluate

class GoldenMetSumTest(unittest.TestCase):
    def test_synthetic_golden_and_calibration(self):
        path = Path(__file__).resolve().parents[2] / "artifacts/golden/met-sum-draft-golden-v1.json"
        self.assertEqual(evaluate(), {"tp": 1, "fp": 0, "fn": 0})
        self.assertEqual(len(hashlib.sha256(path.read_bytes()).hexdigest()), 64)
