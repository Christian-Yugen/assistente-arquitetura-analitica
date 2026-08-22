from __future__ import annotations

import json
from pathlib import Path

from engine.granularity.explicit_key import ExplicitKeyColumnProfile, ExplicitKeySheetProfile, classify_explicit_key
from engine.profiling.explicit_key_grain import profile_explicit_key_header


def evaluate(path: Path = Path("artifacts/golden/grn-expl-draft-golden-v1.json")) -> dict[str, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    true_positives = false_positives = false_negatives = 0
    for case in payload["cases"]:
        columns = tuple(
            ExplicitKeyColumnProfile(
                header=profile_explicit_key_header(column["header"]),
                identifier_signal=column["identifier_signal"],
                sensitive_header=column["sensitive_header"],
                description_header=column["description_header"],
                recognized_date_count=column["recognized_date_count"],
                physical_type=column["physical_type"],
                non_missing_count=column["non_missing_count"],
                distinct_non_missing_count=column["distinct_non_missing_count"],
                formula_count=column["formula_count"],
            )
            for column in case["columns"]
        )
        observed = bool(classify_explicit_key(ExplicitKeySheetProfile(case["observed_row_count"], columns)))
        expected = bool(case["expected"])
        true_positives += int(observed and expected)
        false_positives += int(observed and not expected)
        false_negatives += int(not observed and expected)
    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


if __name__ == "__main__":
    print(evaluate())
