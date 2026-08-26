import unittest
from engine.alerts.low_confidence import LowConfidenceAlertProfile, classify_low_confidence_review

class LowConfidenceAlertTests(unittest.TestCase):
    def test_independent_aggregate_signal_emits_only_blocking_review(self):
        finding = classify_low_confidence_review(LowConfidenceAlertProfile(independent_low_confidence_signal_count=1))
        self.assertEqual(finding["rule_id"], "ALT-LOWCONF-010")
        self.assertTrue(finding["question"]["blocking"])
        self.assertEqual(finding["evidence"][0]["observed_value"], 1)

    def test_missing_signal_or_confirmation_or_sensitivity_or_contract_error_blocks(self):
        self.assertIsNone(classify_low_confidence_review(LowConfidenceAlertProfile()))
        self.assertIsNone(classify_low_confidence_review(LowConfidenceAlertProfile(independent_low_confidence_signal_count=1, human_confidence_confirmation_count=1)))
        self.assertIsNone(classify_low_confidence_review(LowConfidenceAlertProfile(independent_low_confidence_signal_count=1, sensitive_signal_count=1)))
        self.assertIsNone(classify_low_confidence_review(LowConfidenceAlertProfile(independent_low_confidence_signal_count=1, contract_error_count=1)))
