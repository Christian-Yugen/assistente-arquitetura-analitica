import unittest

from engine.quality.numtext import (
    CANONICAL_NUMERIC_TEXT_BASIS,
    NumericTextColumnProfile,
    evaluate_numeric_text,
)


def profile_for_ratio(ratio: float) -> NumericTextColumnProfile:
    return NumericTextColumnProfile(
        name="Campo de teste",
        physical_type="text",
        non_empty_value_count=10_000,
        numeric_text_candidate_count=max(1, round(ratio * 10_000)),
        numeric_text_candidate_ratio=ratio,
        numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
    )


class NumericTextBoundaryTests(unittest.TestCase):
    def test_low_to_medium_boundary_is_deterministic(self):
        self.assertEqual(evaluate_numeric_text(profile_for_ratio(0.0499))[0]["severity"], "low")
        self.assertEqual(evaluate_numeric_text(profile_for_ratio(0.05))[0]["severity"], "medium")

    def test_medium_to_high_boundary_is_deterministic(self):
        self.assertEqual(evaluate_numeric_text(profile_for_ratio(0.4999))[0]["severity"], "medium")
        high = evaluate_numeric_text(profile_for_ratio(0.5))[0]
        self.assertEqual(high["severity"], "high")
        self.assertTrue(high["question"]["blocking"])

    def test_high_ambiguity_uses_the_approved_penalty(self):
        profile = NumericTextColumnProfile(
            name="Campo ambíguo",
            physical_type="text",
            non_empty_value_count=10,
            numeric_text_candidate_count=5,
            numeric_text_candidate_ratio=0.5,
            numeric_text_basis=CANONICAL_NUMERIC_TEXT_BASIS,
            numeric_text_ambiguity_count=10,
        )

        self.assertEqual(evaluate_numeric_text(profile)[0]["confidence"], 0.65)
