from __future__ import annotations

import json
from pathlib import Path

from engine.granularity.event_per_row import EventPerRowSheetProfile, classify_event_per_row


def evaluate(path: Path = Path("artifacts/golden/grn-event-draft-golden-v1.json")) -> dict[str, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    true_positives = false_positives = false_negatives = 0
    for case in payload["cases"]:
        profile = EventPerRowSheetProfile(
            observed_row_count=case["observed_row_count"],
            event_header_eligible_count=case["event_header_eligible_count"],
            explicit_key_candidate_count=case["explicit_key_candidate_count"],
            non_competence_date_candidate_count=case["non_competence_date_candidate_count"],
            excluded_event_marker_count=case["excluded_event_marker_count"],
            event_marker_formula_count=case["event_marker_formula_count"],
            ambiguity_count=case["ambiguity_count"],
        )
        observed = bool(classify_event_per_row(profile))
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
