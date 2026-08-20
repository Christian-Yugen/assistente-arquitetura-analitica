import json
import unittest
from pathlib import Path

from engine.contracts.models import ReconstructedDiagnosis
from engine.contracts.validation import CANONICAL_SCHEMA_PATH, validate_diagnosis_root


EXAMPLES = CANONICAL_SCHEMA_PATH.parent / "examples"


def read_example(name: str) -> dict[str, object]:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


class ReconstructedContractTests(unittest.TestCase):
    def test_validates_minimal_and_complete_examples_with_schema_and_pydantic(self):
        for name in ("minimal.valid.json", "complete.valid.json"):
            example = read_example(name)
            validate_diagnosis_root(example)
            model = ReconstructedDiagnosis.model_validate(example)
            self.assertEqual(model.contract_id, "PM-MVP-PBI-CON-001")

    def test_rejects_unknown_root_property_in_schema_and_pydantic(self):
        invalid = read_example("invalid.unknown-root.json")
        with self.assertRaises(ValueError):
            validate_diagnosis_root(invalid)
        with self.assertRaises(ValueError):
            ReconstructedDiagnosis.model_validate(invalid)

    def test_canonical_artifact_preserves_reconstruction_lineage(self):
        schema = json.loads(CANONICAL_SCHEMA_PATH.read_text(encoding="utf-8"))
        reconstruction = schema["x_reconstruction"]

        self.assertEqual(reconstruction["contract_id"], "PM-MVP-PBI-CON-001")
        self.assertEqual(reconstruction["version"], "1.0.0-reconstructed.1")
        self.assertEqual(reconstruction["source_document"], "Contrato_JSON_Oficial_Diagnostico_Fase2_v1.0.docx")
        self.assertEqual(reconstruction["status"], "approved_reconstructed_for_mvp_draft")
