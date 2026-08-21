import unittest

from engine.contracts.diagnosis import to_diagnosis_fragment
from engine.profiling.categorical_variations import (
    CategoricalVariationProfile,
    NORMALIZATION_BASIS,
    normalize_category_text,
    profile_categorical_variations,
)
from engine.quality.catvar import CategoricalVariationColumnProfile, evaluate_categorical_variations
from engine.quality.registry import QUALITY_RULE_IMPLEMENTATIONS


class CategoricalVariationTests(unittest.TestCase):
    def test_normalizes_only_technical_variations(self):
        self.assertEqual(normalize_category_text("  São-Paulo "), "sao paulo")
        self.assertEqual(normalize_category_text("SÃO   PAULO"), "sao paulo")
        self.assertNotEqual(normalize_category_text("cliente"), normalize_category_text("clientes"))
        self.assertNotEqual(normalize_category_text("adm"), normalize_category_text("administrativo"))

    def test_profiles_collisions_without_retaining_raw_category_values(self):
        profile = profile_categorical_variations(["São-Paulo", "sao paulo", "SÃO PAULO", "Rio"])

        self.assertEqual(profile.text_value_count, 4)
        self.assertEqual(profile.distinct_text_count, 4)
        self.assertEqual(profile.collision_group_count, 1)
        self.assertEqual(profile.affected_value_count, 3)
        self.assertEqual(profile.affected_value_ratio, 0.75)
        self.assertEqual(profile.max_variants_in_group, 3)
        self.assertEqual(profile.dictionary_entry_count, 0)
        self.assertFalse(any("São" in str(value) or "Rio" in str(value) for value in profile.__dict__.values()))

    def test_emits_high_finding_and_blocking_question_without_automatic_merge(self):
        variations = profile_categorical_variations(["São-Paulo", "sao paulo", "Rio", "SÃO PAULO"])
        findings = evaluate_categorical_variations(
            CategoricalVariationColumnProfile(name="Região", physical_type="text", variations=variations)
        )

        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding["rule_id"], "QLT-CATVAR-008")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["confidence"], 0.88)
        self.assertTrue(finding["question"])
        self.assertIn("Validar", finding["recommendation"])
        self.assertNotIn("São-Paulo", str(finding))
        self.assertNotIn("sao paulo", str(finding))

    def test_excludes_high_cardinality_columns_and_profiles_without_collisions(self):
        high_cardinality = CategoricalVariationProfile(
            text_value_count=101,
            distinct_text_count=101,
            collision_group_count=1,
            affected_value_count=2,
            affected_value_ratio=2 / 101,
            max_variants_in_group=2,
            high_cardinality=True,
            normalization_basis=NORMALIZATION_BASIS,
        )
        no_collision = profile_categorical_variations(["Ativo", "Inativo", "Pendente"])

        self.assertEqual(
            evaluate_categorical_variations(
                CategoricalVariationColumnProfile(name="Descrição", physical_type="text", variations=high_cardinality)
            ),
            [],
        )
        self.assertEqual(
            evaluate_categorical_variations(
                CategoricalVariationColumnProfile(name="Status", physical_type="text", variations=no_collision)
            ),
            [],
        )

    def test_adapts_the_high_finding_to_the_canonical_contract(self):
        variations = profile_categorical_variations(["Norte", "norte", "NORTE", "Sul"])
        findings = evaluate_categorical_variations(
            CategoricalVariationColumnProfile(name="Região", physical_type="text", variations=variations)
        )
        fragment = to_diagnosis_fragment(findings, sheet_id="sheet-1", column_id="column-1")

        self.assertEqual(fragment["findings"][0]["rule_id"], "QLT-CATVAR-008")
        self.assertEqual(fragment["findings"][0]["affected_entities"][1], {"entity_type": "column", "entity_id": "column-1"})
        self.assertEqual(len(fragment["questions"]), 1)

    def test_registers_the_rule_by_its_canonical_identifier_after_calibration_gate(self):
        self.assertIs(QUALITY_RULE_IMPLEMENTATIONS["QLT-CATVAR-008"], evaluate_categorical_variations)


if __name__ == "__main__":
    unittest.main()
