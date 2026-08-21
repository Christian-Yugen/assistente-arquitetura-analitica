import json
import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.formula_consistency import (
    FORMULA_CONSISTENCY_BASIS,
    FormulaConsistencyAccumulator,
    FormulaConsistencyProfile,
    profile_formula_consistency,
)
from engine.quality.formula_consistency import FormulaConsistencyColumnProfile, evaluate_formula_consistency
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class FormulaConsistencyTests(unittest.TestCase):
    def test_profiles_only_aggregate_formula_presence(self):
        profile = profile_formula_consistency(
            [("=SUM(A1:A2)", True)] * 19 + [(42, False)]
        )

        self.assertTrue(profile.eligible)
        self.assertEqual(profile.physical_nonempty_count, 20)
        self.assertEqual(profile.formula_count, 19)
        self.assertEqual(profile.nonformula_count, 1)
        self.assertEqual(profile.nonformula_ratio, 0.05)
        self.assertEqual(profile.basis, FORMULA_CONSISTENCY_BASIS)
        serialized = json.dumps(profile.__dict__)
        self.assertNotIn("SUM(A1:A2)", serialized)
        self.assertNotIn("42", serialized)

    def test_excludes_empty_cells_and_rejects_insufficient_or_non_dominant_formula_bases(self):
        all_formulas = profile_formula_consistency([("=A1", True)] * 8 + [(None, False)] * 5)
        below_ratio = profile_formula_consistency([("=A1", True)] * 7 + [(1, False)] * 3)
        eligible = profile_formula_consistency([("=A1", True)] * 8 + [(1, False)] * 2 + [(None, False)] * 4)

        self.assertFalse(all_formulas.eligible)
        self.assertFalse(below_ratio.eligible)
        self.assertTrue(eligible.eligible)
        self.assertEqual(eligible.physical_nonempty_count, 10)

    def test_evaluator_maps_severity_and_rejects_inconsistent_profiles(self):
        low = evaluate_formula_consistency(FormulaConsistencyColumnProfile("Campo", FormulaConsistencyProfile(True, 20, 19, 1, 0.05)))
        medium = evaluate_formula_consistency(FormulaConsistencyColumnProfile("Campo", FormulaConsistencyProfile(True, 20, 18, 2, 0.1)))
        high = evaluate_formula_consistency(FormulaConsistencyColumnProfile("Campo", FormulaConsistencyProfile(True, 20, 16, 4, 0.2)))
        invalid = evaluate_formula_consistency(FormulaConsistencyColumnProfile("Campo", FormulaConsistencyProfile(True, 20, 18, 1, 0.05)))

        self.assertEqual(low[0]["severity"], "low")
        self.assertEqual(medium[0]["severity"], "medium")
        self.assertEqual(high[0]["severity"], "high")
        self.assertEqual(invalid, [])
        self.assertIsNotNone(high[0]["question"])

    def test_contract_and_registry_preserve_private_aggregate_finding(self):
        finding = evaluate_formula_consistency(
            FormulaConsistencyColumnProfile("Campo confidencial", FormulaConsistencyProfile(True, 20, 18, 2, 0.1))
        )[0]
        fragment = to_diagnosis_fragment([finding], sheet_id="sheet-private", column_id="column-private")
        serialized = json.dumps(fragment)

        self.assertIn("QLT-FORMULA-013", QUALITY_RULE_IMPLEMENTATIONS)
        self.assertEqual(fragment["findings"][0]["rule_version"], "0.1.0-provisional.1")
        self.assertNotIn("Campo confidencial", serialized)
        self.assertNotIn("SUM", serialized)

    def test_accumulator_does_not_retain_formula_expression(self):
        accumulator = FormulaConsistencyAccumulator()
        accumulator.consume("=VLOOKUP(A1,External!A:B,2,FALSE)", is_formula=True)
        accumulator.consume(12, is_formula=False)

        serialized = json.dumps(accumulator.__dict__)
        self.assertNotIn("VLOOKUP", serialized)
        self.assertNotIn("External", serialized)
