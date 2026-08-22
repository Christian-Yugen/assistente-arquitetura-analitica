"""Avaliador reproduzível do golden dataset da SEM-STATUS-009."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.numeric_text import infer_physical_type
from engine.profiling.semantic_date import profile_semantic_date
from engine.profiling.semantic_description import profile_semantic_description
from engine.profiling.semantic_identifier import profile_semantic_identifier
from engine.profiling.semantic_status import profile_semantic_status
from engine.semantic.status import SemanticStatusColumnProfile, classify_status


def evaluate() -> dict[str, int]:
    dataset_path = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-status-draft-golden-v1.json"
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    metrics = {"tp": 0, "fp": 0, "fn": 0}
    for case in dataset["cases"]:
        values = case["values"]
        profile = SemanticStatusColumnProfile(
            physical_type=infer_physical_type(values),
            formulas=FormulaConsistencyProfile(formula_count=case["formula_count"]),
            semantic_date=profile_semantic_date(values),
            semantic_identifier=profile_semantic_identifier(case["header"], values),
            semantic_description=profile_semantic_description(case["header"]),
            semantic_status=profile_semantic_status(case["header"], values),
        )
        observed = bool(classify_status(profile))
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
