"""Registro isolado de implementações de relacionamento."""

from engine.relationships.one_to_many import classify_one_to_many_relationship


RELATIONSHIP_RULE_IMPLEMENTATIONS = {
    "REL-ONEMANY-001": classify_one_to_many_relationship,
}
