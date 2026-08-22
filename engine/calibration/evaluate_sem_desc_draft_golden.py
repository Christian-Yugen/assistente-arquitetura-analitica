"""Avaliador reproduzível do golden dataset draft da SEM-DESC-004."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_description import profile_semantic_description
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.semantic.description import SemanticDescriptionColumnProfile, classify_name_or_description


DATASET_PATH = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-desc-draft-golden-v1.json"


def evaluate() -> dict[str, int]:
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    metrics = {"tp": 0, "fp": 0, "fn": 0}
    for case in dataset["cases"]:
        values = case["values"]
        profile = SemanticDescriptionColumnProfile(
            physical_type=infer_physical_type(values),
            formulas=FormulaConsistencyProfile(formula_count=case["formula_count"]),
            semantic_date=profile_semantic_date(values),
            semantic_identifier=profile_semantic_identifier(case["header"], values),
            semantic_description=profile_semantic_description(case["header"]),
        )
        predicted = bool(classify_name_or_description(profile))
        if predicted and case["expected"]:
            metrics["tp"] += 1
        elif predicted:
            metrics["fp"] += 1
        elif case["expected"]:
            metrics["fn"] += 1
    return metrics


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, sort_keys=True))
