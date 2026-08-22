"""Avaliador reproduzível do golden dataset da SEM-DUR-008."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type, profile_numeric_text
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_duration import profile_semantic_duration
from engine.semantic.duration import SemanticDurationColumnProfile, classify_duration


def evaluate() -> dict[str, int]:
    dataset_path = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-dur-draft-golden-v1.json"
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    metrics = {"tp": 0, "fp": 0, "fn": 0}
    for case in dataset["cases"]:
        values = case["values"]
        profile = SemanticDurationColumnProfile(
            physical_type=infer_physical_type(values),
            formulas=FormulaConsistencyProfile(formula_count=case["formula_count"]),
            numeric_text=profile_numeric_text(values),
            semantic_date=profile_semantic_date(values),
            semantic_duration=profile_semantic_duration(case["header"], values),
        )
        observed = bool(classify_duration(profile))
        expected = bool(case["expected"])
        if observed and expected:
            metrics["tp"] += 1
        elif observed and not expected:
            metrics["fp"] += 1
        elif not observed and expected:
            metrics["fn"] += 1
    return metrics


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, sort_keys=True))
