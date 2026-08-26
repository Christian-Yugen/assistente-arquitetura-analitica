from __future__ import annotations
import json
from pathlib import Path
from engine.fact_dimension.conformed_dimension import ConformedDimensionProfile,classify_conformed_dimension
def evaluate() -> dict[str,int]:
 golden=json.loads((Path(__file__).resolve().parents[2]/"artifacts/golden/mdl-dimconf-draft-golden-v1.json").read_text()); totals={"tp":0,"fp":0,"fn":0}
 for case in golden["cases"]:
  emitted=bool(classify_conformed_dimension(ConformedDimensionProfile(**{**golden["profile_defaults"],**case["overrides"]}))); expected=bool(case["expected_finding"])
  if emitted and expected: totals["tp"]+=1
  elif emitted: totals["fp"]+=1
  elif expected: totals["fn"]+=1
 return totals

