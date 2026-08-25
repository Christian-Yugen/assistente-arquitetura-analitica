import json
from pathlib import Path
from engine.metrics.count import CountConceptProfile, classify_count_concept
def evaluate():
    data=json.loads((Path(__file__).resolve().parents[2]/"artifacts/golden/met-count-draft-golden-v1.json").read_text())
    result={"tp":0,"fp":0,"fn":0}
    for case in data["cases"]:
        actual=bool(classify_count_concept(CountConceptProfile(**{**data["profile_defaults"],**case["overrides"]})))
        if actual and case["expected"]: result["tp"]+=1
        elif actual: result["fp"]+=1
        elif case["expected"]: result["fn"]+=1
    return result
