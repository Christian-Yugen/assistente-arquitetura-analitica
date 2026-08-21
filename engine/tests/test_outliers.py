import json
import unittest
from datetime import date

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.outliers import OUTLIER_BASIS, OutlierProfile, profile_outliers
from engine.quality.outliers import OutlierColumnProfile, evaluate_outliers
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class OutlierTests(unittest.TestCase):
    def test_profile_counts_finite_physical_numbers_and_discards_values_and_fences(self):
        profile = profile_outliers(list(range(1, 20)) + [200, True, "201", None, "", float("nan"), float("inf"), date(2026, 8, 20)])

        self.assertTrue(profile.eligible)
        self.assertEqual(profile.physical_nonempty_count, 25)
        self.assertEqual(profile.physical_numeric_count, 20)
        self.assertEqual(profile.upper_outlier_count, 1)
        self.assertEqual(profile.outlier_count, 1)
        self.assertEqual(profile.outlier_ratio, 0.05)
        self.assertEqual(profile.basis, OUTLIER_BASIS)
        serialized = str(profile)
        self.assertNotIn("200", serialized)
        self.assertNotIn("quartile", serialized)

    def test_emits_medium_finding_with_aggregate_evidence_and_human_question(self):
        profile = OutlierProfile(True, 20, 20, 1, 2, 3, 0.15)
        finding = evaluate_outliers(OutlierColumnProfile("Segredo", profile))[0]

        self.assertEqual(finding["rule_id"], "QLT-OUTLIER-012")
        self.assertEqual(finding["severity"], "medium")
        self.assertEqual(finding["confidence"], 0.85)
        self.assertTrue(finding["question"])
        self.assertFalse(finding["question"]["blocking"])
        self.assertNotIn("Segredo", str(finding))

    def test_severity_thresholds_and_human_validation(self):
        low = evaluate_outliers(OutlierColumnProfile("Campo", OutlierProfile(True, 20, 20, 1, 0, 1, 0.05)))[0]
        high = evaluate_outliers(OutlierColumnProfile("Campo", OutlierProfile(True, 20, 20, 3, 2, 5, 0.25)))[0]

        self.assertEqual(low["severity"], "low")
        self.assertTrue(low["question"])
        self.assertEqual(high["severity"], "high")
        self.assertFalse(high["question"]["blocking"])

    def test_excludes_small_base_low_numeric_share_iqr_zero_and_inconsistent_profiles(self):
        cases = [
            OutlierProfile(False, 20, 20, 0, 0, 0, 0.0),
            OutlierProfile(True, 19, 19, 1, 0, 1, 0.05263158),
            OutlierProfile(True, 30, 20, 1, 0, 1, 0.05),
            OutlierProfile(True, 20, 20, 1, 1, 1, 0.05),
            OutlierProfile(True, 20, 20, 1, 0, 1, 0.1, "unapproved_basis"),
        ]
        for profile in cases:
            with self.subTest(profile=profile):
                self.assertEqual(evaluate_outliers(OutlierColumnProfile("Campo", profile)), [])

    def test_adapts_to_canonical_contract_with_aggregate_evidence_only(self):
        profile = OutlierProfile(True, 20, 20, 1, 2, 3, 0.15)
        fragment = to_diagnosis_fragment(
            evaluate_outliers(OutlierColumnProfile("Confidencial", profile)),
            sheet_id="sheet-1",
            column_id="column-1",
        )

        finding = fragment["findings"][0]
        self.assertEqual(finding["rule_version"], "0.1.0-provisional.1")
        serialized = json.dumps(fragment)
        self.assertNotIn("Confidencial", serialized)
        self.assertNotIn("raw_value", serialized)
        self.assertIsNotNone(QUALITY_RULE_IMPLEMENTATIONS["QLT-OUTLIER-012"])
