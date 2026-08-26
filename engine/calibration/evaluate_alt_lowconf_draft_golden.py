import json
from pathlib import Path
from engine.alerts.low_confidence import LowConfidenceAlertProfile, classify_low_confidence_review

def evaluate():
    root = Path(__file__).resolve().parents[2]
    golden = json.loads((root / "artifacts/golden/alt-lowconf-draft-golden-v1.json").read_text())
    result = {"tp": 0, "fp": 0, "fn": 0}
    for case in golden["cases"]:
        emitted = classify_low_confidence_review(LowConfidenceAlertProfile(**{**golden["profile_defaults"], **case["overrides"]})) is not None
        if emitted and case["expected_finding"]: result["tp"] += 1
        elif emitted: result["fp"] += 1
        elif case["expected_finding"]: result["fn"] += 1
    return result
