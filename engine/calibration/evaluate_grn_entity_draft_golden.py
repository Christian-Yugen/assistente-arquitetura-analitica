import json
from pathlib import Path

from engine.granularity.entity_per_row import EntityPerRowSheetProfile, classify_entity_per_row


def evaluate(path: Path = Path("artifacts/golden/grn-entity-draft-golden-v1.json")) -> dict[str, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    true_positives = false_positives = false_negatives = 0
    fields = (
        "observed_row_count",
        "entity_header_eligible_count",
        "explicit_key_candidate_count",
        "descriptive_attribute_candidate_count",
        "non_competence_date_candidate_count",
        "event_candidate_count",
        "measure_candidate_count",
        "sensitive_candidate_count",
        "excluded_entity_marker_count",
        "entity_marker_formula_count",
        "ambiguity_count",
    )
    for case in payload["cases"]:
        observed = bool(classify_entity_per_row(EntityPerRowSheetProfile(**{field: case[field] for field in fields})))
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
