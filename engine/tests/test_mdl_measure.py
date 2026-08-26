import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_mdl_measure_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS
from engine.fact_dimension.stored_measures import StoredMeasuresProfile, classify_stored_measures


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts/golden"


class StoredMeasuresTests(unittest.TestCase):
    def test_signal_and_guards(self):
        candidate = classify_stored_measures(StoredMeasuresProfile(independent_stored_measure_signal_count=1))[0]
        self.assertEqual(candidate["rule_id"], "MDL-MEASURE-015")
        self.assertTrue(candidate["question"]["blocking"])
        profiles = (StoredMeasuresProfile(), StoredMeasuresProfile(independent_stored_measure_signal_count=1, confirmed_measure_design_count=1), StoredMeasuresProfile(independent_stored_measure_signal_count=1, structural_conflict_count=1), StoredMeasuresProfile(independent_stored_measure_signal_count=1, sensitive_signal_count=1), StoredMeasuresProfile(independent_stored_measure_signal_count=1, contract_error_count=1))
        for profile in profiles:
            self.assertEqual(classify_stored_measures(profile), [])

    def test_contract_and_golden(self):
        self.assertEqual(RULE_VERSIONS["MDL-MEASURE-015"], "0.1.0-provisional.1")
        manifest = json.loads((GOLDEN_DIR / "mdl-measure-draft-golden-v1.manifest.json").read_text())
        golden = GOLDEN_DIR / manifest["file"]
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), manifest["calibration"])
        self.assertFalse(manifest["production_authorized"])
