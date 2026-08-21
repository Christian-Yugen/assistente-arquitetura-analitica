import json
from pathlib import Path

from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.profiling.semantic_sensitivity import profile_semantic_sensitivity
from engine.semantic.sensitivity import SemanticSensitivityColumnProfile, classify_sensitivity


GOLDEN = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-sens-draft-golden-v1.json"


def evaluate() -> dict[str, int]:
    tp = fp = fn = 0
    for case in json.loads(GOLDEN.read_text(encoding="utf-8")):
        identifier = profile_semantic_identifier(case["header"], case["values"])
        profile = SemanticSensitivityColumnProfile(
            semantic_sensitivity=profile_semantic_sensitivity(identifier),
        )
        actual = bool(classify_sensitivity(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}
