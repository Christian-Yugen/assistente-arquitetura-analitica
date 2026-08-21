from __future__ import annotations

import json
from pathlib import Path

from engine.fact_dimension.standard_dimension import StandardDimensionSheetProfile, classify_standard_dimension


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/mdl-dimstd-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for case in dataset["cases"]:
        profile = StandardDimensionSheetProfile(
            observed_row_count=case["observed_row_count"],
            grain_available=case["grain_available"],
            individually_unique_identifier_count=case["individually_unique_identifier_count"],
            descriptive_attribute_count=case["descriptive_attribute_count"],
            eligible_measure_column_count=case["eligible_measure_column_count"],
            fully_recognized_temporal_column_count=case["fully_recognized_temporal_column_count"],
        )
        actual = bool(classify_standard_dimension(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
