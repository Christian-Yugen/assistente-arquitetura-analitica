from __future__ import annotations

import json
from pathlib import Path

from engine.fact_dimension.periodic import PeriodicFactSheetProfile, classify_periodic_fact
from engine.profiling.periodic_fact import PeriodicDateProfile


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/mdl-factper-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for case in dataset["cases"]:
        profile = PeriodicFactSheetProfile(
            case["observed_row_count"], case["grain_available"],
            (PeriodicDateProfile(recognized_date_count=case["observed_row_count"], distinct_period_count=case["distinct_period_count"]),),
            case["eligible_measure_column_count"],
        )
        actual = bool(classify_periodic_fact(profile))
        if actual and case["expected"]: tp += 1
        elif actual: fp += 1
        elif case["expected"]: fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
