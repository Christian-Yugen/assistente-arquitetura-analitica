import json
from pathlib import Path

from engine.alerts.quality import CriticalQualityRiskProfile, classify_critical_quality_risk


def evaluate() -> dict[str, int]:
    golden = Path(__file__).resolve().parents[2] / "artifacts/golden/alt-quality-draft-golden-v1.json"
    data = json.loads(golden.read_text())
    result = {"tp": 0, "fp": 0, "fn": 0}
    for case in data["cases"]:
        profile = CriticalQualityRiskProfile(**{**data["profile_defaults"], **case["overrides"]})
        actual = bool(classify_critical_quality_risk(profile))
        if actual and case["expected"]:
            result["tp"] += 1
        elif actual:
            result["fp"] += 1
        elif case["expected"]:
            result["fn"] += 1
    return result
