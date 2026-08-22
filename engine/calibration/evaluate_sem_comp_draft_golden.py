"""Avaliador reproduzível do golden dataset draft da SEM-COMP-002."""

from __future__ import annotations

import json
from pathlib import Path

from engine.profiling.formula_consistency import FormulaConsistencyProfile
from engine.profiling.semantic_competence import profile_semantic_competence
from engine.profiling.semantic_date import profile_semantic_date
from engine.semantic.competence import SemanticCompetenceColumnProfile, classify_competence_date


DATASET_PATH = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-comp-draft-golden-v1.json"


def evaluate() -> dict[str, int]:
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    metrics = {"tp": 0, "fp": 0, "fn": 0}
    for case in dataset["cases"]:
        profile = SemanticCompetenceColumnProfile(
            formulas=FormulaConsistencyProfile(formula_count=case["formula_count"]),
            semantic_date=profile_semantic_date(case["values"]),
            semantic_competence=profile_semantic_competence(case["header"]),
        )
        predicted = bool(classify_competence_date(profile))
        if predicted and case["expected"]:
            metrics["tp"] += 1
        elif predicted:
            metrics["fp"] += 1
        elif case["expected"]:
            metrics["fn"] += 1
    return metrics


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, sort_keys=True))
