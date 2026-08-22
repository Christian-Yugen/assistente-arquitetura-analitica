"""Registro isolado de implementações de relacionamento."""

from engine.relationships.one_to_many import classify_one_to_many_relationship
from engine.relationships.non_unique_one_side import classify_non_unique_one_side_relationship
from engine.relationships.orphan_reference import classify_orphan_reference_relationship


RELATIONSHIP_RULE_IMPLEMENTATIONS = {
    "REL-ONEMANY-001": classify_one_to_many_relationship,
    "REL-NONUNIQ-002": classify_non_unique_one_side_relationship,
    "REL-ORPHAN-003": classify_orphan_reference_relationship,
}
