"""Registro isolado de implementações de granularidade."""

from engine.granularity.composite import classify_composite_grain
from engine.granularity.entity_per_row import classify_entity_per_row
from engine.granularity.event_per_row import classify_event_per_row
from engine.granularity.explicit_key import classify_explicit_key

GRANULARITY_RULE_IMPLEMENTATIONS = {
    "GRN-COMP-001": classify_composite_grain,
    "GRN-ENTITY-003": classify_entity_per_row,
    "GRN-EVENT-004": classify_event_per_row,
    "GRN-EXPL-002": classify_explicit_key,
}
