import json
from pathlib import Path

from engine.metrics.impossible import InsufficientMetricConceptProfile, classify_insufficient_metric_concept


def evaluate() -> dict[str, int]:
    golden = Path(__file__).resolve().parents[2] / "artifacts/golden/met-imposs-draft-golden-v1.json"
    data = json.loads(golden.read_text())
    result = {"tp": 0, "fp": 0, "fn": 0}
    for case in data["cases"]:
        profile = InsufficientMetricConceptProfile(**{**data["profile_defaults"], **case["overrides"]})
        actual = bool(classify_insufficient_metric_concept(profile))
        if actual and case["expected"]:
            result["tp"] += 1
        elif actual:
            result["fp"] += 1
        elif case["expected"]:
            result["fn"] += 1
    return result
