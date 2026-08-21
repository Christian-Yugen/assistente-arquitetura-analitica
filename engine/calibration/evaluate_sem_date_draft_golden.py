"""Calibração determinística da SEM-DATE-001 sobre o golden dataset assinado."""
from __future__ import annotations
import json
from pathlib import Path
from engine.profiling.semantic_date import profile_semantic_date
from engine.semantic.date_generic import SemanticDateColumnProfile, classify_date_generic

GOLDEN = Path(__file__).resolve().parents[2] / "artifacts/golden/sem-date-draft-golden-v1.json"

def evaluate() -> dict[str, int]:
    cases = json.loads(GOLDEN.read_text(encoding="utf-8"))["cases"]
    tp = fp = fn = 0
    for case in cases:
        actual = bool(classify_date_generic(SemanticDateColumnProfile("Data", profile_semantic_date(case["values"]))))
        expected = case["expected"]
        tp += int(actual and expected); fp += int(actual and not expected); fn += int(not actual and expected)
    return {"tp": tp, "fp": fp, "fn": fn}

if __name__ == "__main__":
    print(json.dumps(evaluate(), sort_keys=True))
