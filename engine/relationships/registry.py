"""Registro isolado de implementações de relacionamento."""

from engine.relationships.one_to_many import classify_one_to_many_relationship
from engine.relationships.non_unique_one_side import classify_non_unique_one_side_relationship
from engine.relationships.orphan_reference import classify_orphan_reference_relationship
from engine.relationships.many_to_many import classify_many_to_many_relationship
from engine.relationships.direct_fact import classify_direct_fact_relationship
from engine.relationships.ambiguous_path import classify_ambiguous_relationship_path
from engine.relationships.bidirectional_filter import classify_bidirectional_filter_review
from engine.relationships.composite_key import classify_composite_relationship_key
from engine.relationships.conformed_dimension import classify_conformed_dimension


RELATIONSHIP_RULE_IMPLEMENTATIONS = {
    "REL-ONEMANY-001": classify_one_to_many_relationship,
    "REL-NONUNIQ-002": classify_non_unique_one_side_relationship,
    "REL-ORPHAN-003": classify_orphan_reference_relationship,
    "REL-MANYMANY-004": classify_many_to_many_relationship,
    "REL-FACTFACT-006": classify_direct_fact_relationship,
    "REL-AMBIG-007": classify_ambiguous_relationship_path,
    "REL-BIDIR-008": classify_bidirectional_filter_review,
    "REL-COMPKEY-009": classify_composite_relationship_key,
    "REL-CONFORMED-010": classify_conformed_dimension,
}
