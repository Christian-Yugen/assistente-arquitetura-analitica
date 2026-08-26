import hashlib
import json
import unittest
from pathlib import Path

from engine.calibration.evaluate_rel_bridge_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS
from engine.relationships.bridge_need import BridgeNeedProfile, classify_bridge_need


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "artifacts/golden"


class BridgeNeedTests(unittest.TestCase):
    def test_signal_and_guards(self):
        candidate = classify_bridge_need(BridgeNeedProfile(independent_bridge_need_signal_count=1))
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate["rule_id"], "REL-BRIDGE-005")
        self.assertTrue(candidate["question"]["blocking"])
        profiles = (BridgeNeedProfile(), BridgeNeedProfile(independent_bridge_need_signal_count=1, confirmed_relationship_design_count=1), BridgeNeedProfile(independent_bridge_need_signal_count=1, structural_conflict_count=1), BridgeNeedProfile(independent_bridge_need_signal_count=1, sensitive_signal_count=1), BridgeNeedProfile(independent_bridge_need_signal_count=1, contract_error_count=1))
        for profile in profiles:
            self.assertIsNone(classify_bridge_need(profile))

    def test_contract_and_golden(self):
        self.assertEqual(RULE_VERSIONS["REL-BRIDGE-005"], "0.1.0-provisional.1")
        manifest = json.loads((GOLDEN_DIR / "rel-bridge-draft-golden-v1.manifest.json").read_text())
        golden = GOLDEN_DIR / manifest["file"]
        self.assertEqual(hashlib.sha256(golden.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(evaluate(), manifest["calibration"])
        self.assertFalse(manifest["production_authorized"])
