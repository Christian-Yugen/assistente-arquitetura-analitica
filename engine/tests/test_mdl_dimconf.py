import hashlib,json,unittest
from pathlib import Path
from engine.fact_dimension.conformed_dimension import ConformedDimensionProfile,classify_conformed_dimension
from engine.calibration.evaluate_mdl_dimconf_draft_golden import evaluate
from engine.contracts.diagnosis import RULE_VERSIONS
GOLDEN_DIR=Path(__file__).resolve().parents[2]/"artifacts/golden"
class ConformedDimensionTests(unittest.TestCase):
 def test_signal_and_guards(self):
  candidate=classify_conformed_dimension(ConformedDimensionProfile(independent_conformed_dimension_signal_count=1))[0]; self.assertEqual(candidate["rule_id"],"MDL-DIMCONF-005"); self.assertTrue(candidate["question"]["blocking"])
  for p in (ConformedDimensionProfile(),ConformedDimensionProfile(independent_conformed_dimension_signal_count=1,confirmed_dimension_design_count=1),ConformedDimensionProfile(independent_conformed_dimension_signal_count=1,structural_conflict_count=1),ConformedDimensionProfile(independent_conformed_dimension_signal_count=1,sensitive_signal_count=1),ConformedDimensionProfile(independent_conformed_dimension_signal_count=1,contract_error_count=1)): self.assertEqual(classify_conformed_dimension(p),[])
 def test_contract_and_golden(self):
  self.assertEqual(RULE_VERSIONS["MDL-DIMCONF-005"],"0.1.0-provisional.1")
  manifest=json.loads((GOLDEN_DIR/"mdl-dimconf-draft-golden-v1.manifest.json").read_text()); path=GOLDEN_DIR/manifest["file"]; self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest["sha256"]); self.assertEqual(evaluate(),manifest["calibration"]); self.assertFalse(manifest["production_authorized"])
