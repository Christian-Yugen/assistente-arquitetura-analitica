import json
from pathlib import Path

from engine.metrics.semiadditive import SemiadditiveConceptProfile, classify_semiadditive_concept


def evaluate() -> dict[str, int]:
    data = json.loads((Path(__file__).resolve().parents[2] / "artifacts/golden/met-semiadd-draft-golden-v1.json").read_text())
    result = {"tp": 0, "fp": 0, "fn": 0}
    for case in data["cases"]:
        actual = bool(classify_semiadditive_concept(SemiadditiveConceptProfile(**{**data["profile_defaults"], **case["overrides"]})))
        if actual and case["expected"]:
            result["tp"] += 1
        elif actual:
            result["fp"] += 1
        elif case["expected"]:
            result["fn"] += 1
    return result
