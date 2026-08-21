from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import profile_numeric_text
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_quantity import profile_semantic_quantity
from engine.semantic.quantity import SemanticQuantityColumnProfile, classify_quantity


GOLDEN = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-qty-draft-golden-v1.json"


def evaluate() -> dict[str, int]:
    tp = fp = fn = 0
    for case in json.loads(GOLDEN.read_text(encoding="utf-8")):
        values = case["values"]
        profile = SemanticQuantityColumnProfile(
            physical_type=case["physical_type"],
            formulas=FormulaConsistencyProfile(formula_count=case["formula_count"]),
            numeric_text=profile_numeric_text(values),
            semantic_date=profile_semantic_date(values),
            semantic_quantity=profile_semantic_quantity(case["header"], values),
        )
        actual = bool(classify_quantity(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}
