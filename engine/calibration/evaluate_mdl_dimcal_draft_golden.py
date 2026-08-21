from __future__ import annotations

import json
from pathlib import Path

from engine.fact_dimension.calendar_dimension import CalendarDimensionSheetProfile, classify_calendar_dimension
from engine.profiling.calendar_dimension import CalendarDateProfile


def evaluate() -> dict[str, int]:
    path = Path(__file__).resolve().parents[2] / "artifacts/golden/mdl-dimcal-draft-golden-v1.json"
    dataset = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for case in dataset["cases"]:
        profile = CalendarDimensionSheetProfile(
            observed_row_count=case["observed_row_count"],
            grain_available=case["grain_available"],
            calendar_dates=tuple(CalendarDateProfile(**item) for item in case["calendar_dates"]),
            eligible_measure_column_count=case["eligible_measure_column_count"],
        )
        actual = bool(classify_calendar_dimension(profile))
        if actual and case["expected"]:
            tp += 1
        elif actual:
            fp += 1
        elif case["expected"]:
            fn += 1
    return {"tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    print(evaluate())
