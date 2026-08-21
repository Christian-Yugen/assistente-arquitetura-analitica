"""Registro isolado de implementações de granularidade."""

from engine.granularity.composite import classify_composite_grain

GRANULARITY_RULE_IMPLEMENTATIONS = {"GRN-COMP-001": classify_composite_grain}
