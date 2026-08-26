import hashlib,json,unittest
from pathlib import Path
from engine.fact_dimension.accumulated_snapshot import AccumulatedSnapshotProfile,classify_accumulated_snapshot
from engine.calibration.evaluate_mdl_factacc_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS
GOLDEN_DIR=Path(__file__).resolve().parents[2]/"artifacts/golden"
class AccumulatedSnapshotTests(unittest.TestCase):
 def test_signal_and_guards(self):
  candidate=classify_accumulated_snapshot(AccumulatedSnapshotProfile(independent_accumulated_snapshot_signal_count=1))[0]; self.assertEqual(candidate["rule_id"],"MDL-FACTACC-003"); self.assertTrue(candidate["question"]["blocking"])
  for p in (AccumulatedSnapshotProfile(),AccumulatedSnapshotProfile(independent_accumulated_snapshot_signal_count=1,confirmed_accumulated_snapshot_count=1),AccumulatedSnapshotProfile(independent_accumulated_snapshot_signal_count=1,structural_conflict_count=1),AccumulatedSnapshotProfile(independent_accumulated_snapshot_signal_count=1,sensitive_signal_count=1),AccumulatedSnapshotProfile(independent_accumulated_snapshot_signal_count=1,contract_error_count=1)): self.assertEqual(classify_accumulated_snapshot(p),[])
 def test_contract_and_golden(self):
  self.assertEqual(RULE_VERSIONS["MDL-FACTACC-003"],"0.1.0-provisional.1")
  manifest=json.loads((GOLDEN_DIR/"mdl-factacc-draft-golden-v1.manifest.json").read_text()); path=GOLDEN_DIR/manifest["file"]; self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest["sha256"]); self.assertEqual(evaluate(),manifest["calibration"]); self.assertFalse(manifest["production_authorized"])
