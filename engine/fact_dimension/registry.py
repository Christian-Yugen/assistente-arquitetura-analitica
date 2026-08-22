"""Registro isolado de implementações de fato e dimensão."""

from engine.fact_dimension.calendar_dimension import classify_calendar_dimension
from engine.fact_dimension.fact_without_grain import classify_fact_without_defined_grain
from engine.fact_dimension.periodic import classify_periodic_fact
from engine.fact_dimension.standard_dimension import classify_standard_dimension
from engine.fact_dimension.transactional import classify_transactional_fact


FACT_DIMENSION_RULE_IMPLEMENTATIONS = {
    "MDL-FACTPER-001": classify_periodic_fact,
    "MDL-FACTTXN-002": classify_transactional_fact,
    "MDL-FACTNOGRAIN-019": classify_fact_without_defined_grain,
    "MDL-DIMSTD-004": classify_standard_dimension,
    "MDL-DIMCAL-006": classify_calendar_dimension,
}
