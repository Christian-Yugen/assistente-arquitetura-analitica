from __future__ import annotations

import json
from pathlib import Path

from engine.relationships.composite_key import CompositeRelationshipKeyPairProfile, classify_composite_relationship_key


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/rel-compkey-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for case in dataset["cases"]:
        values = {**dataset["profile_defaults"], **case["overrides"]}
        actual = bool(classify_composite_relationship_key(CompositeRelationshipKeyPairProfile(**values)))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
