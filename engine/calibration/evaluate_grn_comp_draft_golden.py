from __future__ import annotations

import json
from pathlib import Path

from engine.granularity.composite import CompositeGrainSheetProfile, classify_composite_grain
from engine.profiling.composite_grain import CompositeGrainAccumulator


def evaluate(path: Path) -> dict[str, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for case in payload["cases"]:
        accumulator = CompositeGrainAccumulator(((0, 1),))
        for row in case["rows"]:
            accumulator.consume(tuple(row))
        observed = bool(classify_composite_grain(CompositeGrainSheetProfile(accumulator.finalize(eligible_pair_count=1), frozenset({0, 1}))))
        expected = bool(case["expected"])
        tp += int(observed and expected)
        fp += int(observed and not expected)
        fn += int(not observed and expected)
    return {"true_positives": tp, "false_positives": fp, "false_negatives": fn}


if __name__ == "__main__":
    print(evaluate(Path("artifacts/golden/grn-comp-draft-golden-v1.json")))
