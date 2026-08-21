from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import profile_numeric_text
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_percentage import profile_semantic_percentage
from engine.semantic.percentage import SemanticPercentageColumnProfile, classify_percentage


GOLDEN = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-pct-draft-golden-v1.json"


def evaluate() -> dict[str, int]:
    tp = fp = fn = 0
    for case in json.loads(GOLDEN.read_text(encoding="utf-8")):
        values = case["values"]
        profile = SemanticPercentageColumnProfile(
            physical_type=case["physical_type"],
            formulas=FormulaConsistencyProfile(formula_count=case["formula_count"]),
            numeric_text=profile_numeric_text(values),
            semantic_date=profile_semantic_date(values),
            semantic_percentage=profile_semantic_percentage(case["header"], values),
        )
        actual = bool(classify_percentage(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}
