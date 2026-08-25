import json
from pathlib import Path
from engine.metrics.minmax import MinMaxConceptProfile, classify_minmax_concept
def evaluate():
    data=json.loads((Path(__file__).resolve().parents[2]/"artifacts/golden/met-minmax-draft-golden-v1.json").read_text())
    result={"tp":0,"fp":0,"fn":0}
    for case in data["cases"]:
        actual=bool(classify_minmax_concept(MinMaxConceptProfile(**{**data["profile_defaults"],**case["overrides"]})))
        if actual and case["expected"]: result["tp"]+=1
        elif actual: result["fp"]+=1
        elif case["expected"]: result["fn"]+=1
    return result
