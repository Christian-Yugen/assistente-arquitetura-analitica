import json
import unittest
from copy import deepcopy

from engine.contracts.execution_profile import (
    PROFILE_PATH,
    REQUIRED_GOVERNED_OUTPUT_PATHS,
    _read_path,
    expected_governed_output_values,
    load_authorized_draft_profile,
    validate_governed_output,
)
from engine.catalog import executable_rule_count
from engine.pipeline.quality_diagnosis import build_column_analysis_context, execute_quality_diagnosis
from engine.tests.test_numtext_pipeline import METADATA


class DraftExecutionProfileTests(unittest.TestCase):
    @staticmethod
    def _set_path(payload: dict[str, object], path: str, value: object) -> None:
        current: object = payload
        segments = path.split(".")
        for segment in segments[:-1]:
            if "[" in segment:
                key, index = segment.removesuffix("]").split("[")
                current = current[key][int(index)]  # type: ignore[index]
            else:
                current = current[segment]  # type: ignore[index]
        last = segments[-1]
        if "[" in last:
            key, index = last.removesuffix("]").split("[")
            current[key][int(index)] = value  # type: ignore[index]
        else:
            current[last] = value  # type: ignore[index]

    @staticmethod
    def _divergent_value(value: object) -> object:
        if isinstance(value, bool):
            return not value
        if isinstance(value, (int, float)):
            return value + 1
        if isinstance(value, str):
            return f"{value}__unauthorized"
        if isinstance(value, list):
            return ["unauthorized"]
        if isinstance(value, dict):
            return {"unauthorized": True}
        return "unauthorized"
    def test_loads_only_the_governed_draft_profile(self):
        profile = load_authorized_draft_profile()

        self.assertEqual(profile.profile_id, "PM-MVP-PBI-DRAFT-EXECUTION-001")
        self.assertEqual(profile.catalog_target_rule_count, 95)
        self.assertEqual(profile.engine_version, "0.1.0")
        self.assertIn("{finding_count}", profile.summary_template)
        self.assertEqual(set(profile.governed_output_paths), REQUIRED_GOVERNED_OUTPUT_PATHS)

    def test_profile_artifact_explicitly_blocks_production(self):
        payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

        self.assertEqual(payload["status"], "authorized_for_mvp_draft")
        self.assertFalse(payload["governance"]["production_ready"])
        self.assertEqual(payload["governance"]["approved_by_gate"], "CONTRACT-RECONSTRUCTION-001")

    def test_rejects_any_divergence_in_the_governed_output_allowlist(self):
        profile = load_authorized_draft_profile()
        context = build_column_analysis_context(
            sheet_id="00000000-0000-4000-8000-000000000030",
            column_id="00000000-0000-4000-8000-000000000031",
            column_name="Valor",
            values=["10", "20"],
            sheet_name="Dados",
            sheet_position=0,
            sheet_visibility="visible",
            column_position=0,
        )
        diagnosis = execute_quality_diagnosis([context], metadata=METADATA)
        executed_rule_count = executable_rule_count()
        validate_governed_output(diagnosis, profile=profile, executed_rule_count=executed_rule_count)
        expected = expected_governed_output_values(diagnosis, profile=profile, executed_rule_count=executed_rule_count)

        self.assertEqual(set(expected), REQUIRED_GOVERNED_OUTPUT_PATHS)
        self.assertEqual(set(expected), set(profile.governed_output_paths))
        self.assertEqual(
            {path: _read_path(diagnosis, path) for path in profile.governed_output_paths},
            expected,
        )

        for path in profile.governed_output_paths:
            invalid = deepcopy(diagnosis)
            self._set_path(invalid, path, self._divergent_value(_read_path(diagnosis, path)))
            with self.assertRaises(ValueError, msg=path):
                validate_governed_output(invalid, profile=profile, executed_rule_count=executed_rule_count)
