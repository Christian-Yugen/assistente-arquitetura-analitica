import json
from pathlib import Path
from engine.metrics.sum import SumConceptProfile, classify_sum_concept

def evaluate() -> dict[str, int]:
    dataset = json.loads((Path(__file__).resolve().parents[2] / "artifacts/golden/met-sum-draft-golden-v1.json").read_text())
    counts = {"tp": 0, "fp": 0, "fn": 0}
    for case in dataset["cases"]:
        actual = bool(classify_sum_concept(SumConceptProfile(**{**dataset["profile_defaults"], **case["overrides"]})))
        if actual and case["expected"]: counts["tp"] += 1
        elif actual: counts["fp"] += 1
        elif case["expected"]: counts["fn"] += 1
    return counts
