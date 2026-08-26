import hashlib,json,unittest
from pathlib import Path
from engine.alerts.inconsistent_grain import InconsistentGrainProfile,classify_inconsistent_grain
from engine.calibration.evaluate_grn_incons_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS,to_diagnosis_fragment
GOLDEN_DIR=Path(__file__).resolve().parents[2]/"artifacts/golden"
class InconsistentGrainTests(unittest.TestCase):
 def test_signal_and_guards(self):
  finding=classify_inconsistent_grain(InconsistentGrainProfile(independent_inconsistent_grain_signal_count=1)); self.assertEqual(finding["rule_id"],"GRN-INCONS-009"); self.assertTrue(finding["question"]["blocking"])
  for p in (InconsistentGrainProfile(),InconsistentGrainProfile(independent_inconsistent_grain_signal_count=1,confirmed_grain_count=1),InconsistentGrainProfile(independent_inconsistent_grain_signal_count=1,structural_conflict_count=1),InconsistentGrainProfile(independent_inconsistent_grain_signal_count=1,sensitive_signal_count=1),InconsistentGrainProfile(independent_inconsistent_grain_signal_count=1,contract_error_count=1)): self.assertIsNone(classify_inconsistent_grain(p))
 def test_contract_and_golden(self):
  f=classify_inconsistent_grain(InconsistentGrainProfile(independent_inconsistent_grain_signal_count=2)); frag=to_diagnosis_fragment([f],sheet_id="opaque",column_id=None); self.assertEqual(RULE_VERSIONS["GRN-INCONS-009"],"0.1.0-provisional.1"); self.assertEqual(frag["findings"][0]["evidence"][0]["observed"],{"observed_value":2})
  manifest=json.loads((GOLDEN_DIR/"grn-incons-draft-golden-v1.manifest.json").read_text()); path=GOLDEN_DIR/manifest["file"]; self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest["sha256"]); self.assertEqual(evaluate(),manifest["calibration"]); self.assertFalse(manifest["production_authorized"])
