import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from engine.profiling.workbook import profile_workbook_with_relationship_pairs


class RelationshipWorkbookProfilingTests(unittest.TestCase):
    def create_workbook(self) -> Path:
        handle = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        handle.close()
        workbook = Workbook()
        dimension = workbook.active
        dimension.title = "Clientes Confidenciais"
        dimension.append(["codigo", "descricao"])
        dimension.append(["C-001", "Cliente reservado um"])
        dimension.append(["C-002", "Cliente reservado dois"])
        dimension.append(["C-003", "Cliente reservado três"])
        fact = workbook.create_sheet("Pedidos Privados")
        fact.append(["cod", "valor"])
        fact.append(["C-001", 10])
        fact.append(["C-001", 20])
        fact.append(["C-003", 30])
        fact.append(["C-003", 40])
        workbook.save(handle.name)
        return Path(handle.name)

    def test_reduces_cross_sheet_matches_to_private_aggregated_signals(self):
        path = self.create_workbook()
        try:
            profile = profile_workbook_with_relationship_pairs(path)
        finally:
            path.unlink(missing_ok=True)

        self.assertEqual(len(profile.columns), 4)
        self.assertEqual(len(profile.relationship_pair_signals), 2)
        positive_direction = next(
            signal for signal in profile.relationship_pair_signals if signal.referential_coverage_ratio == 1.0
        )
        self.assertTrue(positive_direction.source_complete)
        self.assertTrue(positive_direction.source_unique)
        self.assertTrue(positive_direction.target_complete)
        self.assertFalse(positive_direction.target_unique)
        self.assertEqual(positive_direction.source_distinct_count, 3)
        self.assertEqual(positive_direction.target_distinct_count, 2)
        self.assertEqual(positive_direction.referential_coverage_ratio, 1.0)

        rendered = repr(profile.relationship_pair_signals)
        for prohibited in (
            "Clientes Confidenciais",
            "Pedidos Privados",
            "codigo",
            "descricao",
            "C-001",
            "Cliente reservado um",
        ):
            self.assertNotIn(prohibited, rendered)
