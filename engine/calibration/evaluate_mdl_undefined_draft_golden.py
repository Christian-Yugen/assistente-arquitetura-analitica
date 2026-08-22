from __future__ import annotations

import json
from pathlib import Path

from engine.fact_dimension.undefined_classification import (
    UndefinedTableClassificationSheetProfile,
    classify_undefined_table_classification,
)


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/mdl-undefined-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    profile_fields = (
        "observed_row_count",
        "physical_column_count",
        "evaluated_table_classifier_count",
        "positive_table_classification_count",
        "classification_conflict_count",
        "formula_column_count",
        "sensitive_candidate_count",
        "classification_ambiguity_count",
    )
    for case in dataset["cases"]:
        profile = UndefinedTableClassificationSheetProfile(**{
            field: case[field] for field in profile_fields
        })
        actual = bool(classify_undefined_table_classification(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
