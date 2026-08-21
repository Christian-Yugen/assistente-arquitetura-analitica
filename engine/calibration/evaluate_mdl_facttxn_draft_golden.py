from __future__ import annotations

import json
from pathlib import Path

from engine.fact_dimension.transactional import TransactionalFactSheetProfile, classify_transactional_fact
from engine.profiling.transactional_fact import TransactionalDateProfile


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/mdl-facttxn-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for case in dataset["cases"]:
        profile = TransactionalFactSheetProfile(
            case["observed_row_count"],
            case["grain_available"],
            (TransactionalDateProfile(
                recognized_date_count=case["recognized_date_count"],
                distinct_date_count=case["distinct_date_count"],
            ),),
            case["eligible_measure_column_count"],
        )
        actual = bool(classify_transactional_fact(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
