from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.semantic.identifier import SemanticIdentifierColumnProfile, classify_identifier

GOLDEN = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-id-draft-golden-v1.json"


def evaluate() -> dict[str, int]:
    tp = fp = fn = 0
    for case in json.loads(GOLDEN.read_text(encoding="utf-8")):
        profile = profile_semantic_identifier(case["header"], case["values"])
        actual = bool(classify_identifier(SemanticIdentifierColumnProfile(case["physical_type"], case["formula_count"], profile)))
        if actual and case["expected"]: tp += 1
        elif actual: fp += 1
        elif case["expected"]: fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}
