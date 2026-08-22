from __future__ import annotations

import json
from pathlib import Path

from engine.fact_dimension.fact_without_grain import (
    FactWithoutDefinedGrainSheetProfile,
    classify_fact_without_defined_grain,
)


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/mdl-factnograin-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    profile_fields = (
        "observed_row_count",
        "eligible_numeric_measure_count",
        "fact_signal_count",
        "active_grain_hypothesis_count",
        "dimensional_candidate_count",
        "formula_column_count",
        "sensitive_candidate_count",
        "incompatible_temporal_signal_count",
        "ambiguity_count",
    )
    for case in dataset["cases"]:
        profile = FactWithoutDefinedGrainSheetProfile(**{
            field: case[field] for field in profile_fields
        })
        actual = bool(classify_fact_without_defined_grain(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
