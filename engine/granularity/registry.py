"""Registro isolado de implementações de granularidade."""

from engine.granularity.composite import classify_composite_grain
from engine.granularity.explicit_key import classify_explicit_key

GRANULARITY_RULE_IMPLEMENTATIONS = {
    "GRN-COMP-001": classify_composite_grain,
    "GRN-EXPL-002": classify_explicit_key,
}
