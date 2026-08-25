import unittest

from engine.catalog import RuleExecutionUnavailableError, execute_registered_rule, get_rule_execution_record
from engine.contracts.diagnosis import RULE_VERSIONS, to_metric_fragment
from engine.metrics.completion import CompletionRateConceptProfile
from engine.metrics.rate import RateConceptProfile
from engine.metrics.absolute_delta import AbsoluteDeltaConceptProfile


class MetricContractTests(unittest.TestCase):
    def test_completion_metric_is_versioned_and_executes_only_in_the_draft_profile(self):
        record = get_rule_execution_record("MET-COMPL-001")

        self.assertEqual(RULE_VERSIONS["MET-COMPL-001"], "0.1.0-provisional.1")
        self.assertEqual(record.status, "executable_draft")
        candidate = execute_registered_rule(
            "MET-COMPL-001",
            CompletionRateConceptProfile(
                row_count=20,
                physical_column_count=2,
                status_candidate_count=1,
                has_defined_grain=True,
            ),
        )
        self.assertIsNotNone(candidate)

    def test_metric_projection_keeps_formula_conceptual_and_values_private(self):
        candidate = {
            "rule_id": "MET-COMPL-001",
            "metric_type": "completion_rate_conceptual_metric_candidate",
            "confidence": 0.60,
            "severity": "review_required",
            "conceptual_formula": "completed_items / eligible_items",
            "evidence": {"row_count": 20, "status_candidate_count": 1},
            "question": {
                "text": "Defina estados e denominador.",
                "reason": "Sem cálculo automático.",
                "question_type": "single_choice",
                "priority": "high",
                "blocking": True,
                "options": ["Definir", "Não recomendar"],
            },
        }
        fragment = to_metric_fragment([candidate], sheet_id="opaque-sheet")
        metric = fragment["metrics"][0]

        self.assertEqual(metric["status"], "conceptual_review")
        self.assertEqual(metric["conceptual_formula"], "completed_items / eligible_items")
        self.assertNotIn("dax", metric)
        self.assertNotIn("status_values", metric["evidence"])

    def test_rate_metric_is_versioned_and_projects_without_field_identity_or_calculation(self):
        candidate = execute_registered_rule(
            "MET-RATE-007",
            RateConceptProfile(
                row_count=20,
                physical_column_count=2,
                numerator_candidate_count=1,
                denominator_candidate_count=1,
                has_defined_grain=True,
            ),
        )
        self.assertEqual(RULE_VERSIONS["MET-RATE-007"], "0.1.0-provisional.1")
        self.assertEqual(candidate["conceptual_formula"], "eligible_numerator / eligible_denominator")
        metric = to_metric_fragment([candidate], sheet_id="opaque-sheet")["metrics"][0]
        self.assertEqual(metric["status"], "conceptual_review")
        self.assertNotIn("dax", metric)
        self.assertNotIn("power_query", metric)
        self.assertNotIn("column_id", metric["evidence"])
        self.assertNotIn("value", metric["evidence"])

    def test_absolute_delta_metric_is_versioned_and_projects_without_calculation_or_field_identity(self):
        candidate = execute_registered_rule(
            "MET-ABSDELTA-008",
            AbsoluteDeltaConceptProfile(
                row_count=20,
                physical_column_count=2,
                actual_candidate_count=1,
                baseline_candidate_count=1,
                has_defined_grain=True,
            ),
        )
        self.assertEqual(RULE_VERSIONS["MET-ABSDELTA-008"], "0.1.0-provisional.1")
        self.assertEqual(candidate["conceptual_formula"], "eligible_actual - eligible_baseline")
        metric = to_metric_fragment([candidate], sheet_id="opaque-sheet")["metrics"][0]
        self.assertEqual(metric["status"], "conceptual_review")
        self.assertNotIn("dax", metric)
        self.assertNotIn("power_query", metric)
        self.assertNotIn("column_id", metric["evidence"])
        self.assertNotIn("value", metric["evidence"])
