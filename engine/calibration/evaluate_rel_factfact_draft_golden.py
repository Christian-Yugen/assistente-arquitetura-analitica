from __future__ import annotations

import json
from pathlib import Path

from engine.relationships.direct_fact import DirectFactRelationshipPairProfile, classify_direct_fact_relationship


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/rel-factfact-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for case in dataset["cases"]:
        values = {**dataset["profile_defaults"], **case["overrides"]}
        actual = bool(classify_direct_fact_relationship(DirectFactRelationshipPairProfile(**values)))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
