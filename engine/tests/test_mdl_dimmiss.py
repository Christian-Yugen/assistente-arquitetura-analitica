import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_mdl_dimmiss_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS
from engine.fact_dimension.missing_dimension import MissingDimensionProfile, classify_missing_dimension


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts/golden"


class MissingDimensionTests(unittest.TestCase):
    def test_signal_and_guards(self):
        candidate = classify_missing_dimension(MissingDimensionProfile(independent_missing_dimension_signal_count=1))[0]
        self.assertEqual(candidate["rule_id"], "MDL-DIMMISS-017")
        self.assertTrue(candidate["question"]["blocking"])
        profiles = (MissingDimensionProfile(), MissingDimensionProfile(independent_missing_dimension_signal_count=1, confirmed_dimension_design_count=1), MissingDimensionProfile(independent_missing_dimension_signal_count=1, structural_conflict_count=1), MissingDimensionProfile(independent_missing_dimension_signal_count=1, sensitive_signal_count=1), MissingDimensionProfile(independent_missing_dimension_signal_count=1, contract_error_count=1))
        for profile in profiles:
            self.assertEqual(classify_missing_dimension(profile), [])

    def test_contract_and_golden(self):
        self.assertEqual(RULE_VERSIONS["MDL-DIMMISS-017"], "0.1.0-provisional.1")
        manifest = json.loads((GOLDEN_DIR / "mdl-dimmiss-draft-golden-v1.manifest.json").read_text())
        golden = GOLDEN_DIR / manifest["file"]
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), manifest["calibration"])
        self.assertFalse(manifest["production_authorized"])
