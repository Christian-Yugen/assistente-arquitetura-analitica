"""Registro isolado de implementações de fato e dimensão."""

from engine.fact_dimension.calendar_dimension import classify_calendar_dimension
from engine.fact_dimension.fact_without_grain import classify_fact_without_defined_grain
from engine.fact_dimension.periodic import classify_periodic_fact
from engine.fact_dimension.standard_dimension import classify_standard_dimension
from engine.fact_dimension.transactional import classify_transactional_fact
from engine.fact_dimension.undefined_classification import classify_undefined_table_classification
from engine.fact_dimension.accumulated_snapshot import classify_accumulated_snapshot
from engine.fact_dimension.conformed_dimension import classify_conformed_dimension
from engine.fact_dimension.role_dimension import classify_role_dimension
from engine.fact_dimension.degenerate_dimension import classify_degenerate_dimension
from engine.fact_dimension.bridge_table import classify_bridge_table
from engine.fact_dimension.auxiliary_table import classify_auxiliary_table
from engine.fact_dimension.parameter_table import classify_parameter_table
from engine.fact_dimension.flat_table import classify_flat_table
from engine.fact_dimension.mixed_table import classify_mixed_table
from engine.fact_dimension.repeated_attributes import classify_repeated_attributes
from engine.fact_dimension.stored_measures import classify_stored_measures
from engine.fact_dimension.extractable_dimension import classify_extractable_dimension


FACT_DIMENSION_RULE_IMPLEMENTATIONS = {
    "MDL-FACTPER-001": classify_periodic_fact,
    "MDL-FACTTXN-002": classify_transactional_fact,
    "MDL-FACTNOGRAIN-019": classify_fact_without_defined_grain,
    "MDL-DIMSTD-004": classify_standard_dimension,
    "MDL-DIMCAL-006": classify_calendar_dimension,
    "MDL-UNDEFINED-020": classify_undefined_table_classification,
    "MDL-FACTACC-003": classify_accumulated_snapshot,
    "MDL-DIMCONF-005": classify_conformed_dimension,
    "MDL-DIMROLE-007": classify_role_dimension,
    "MDL-DIMDEG-008": classify_degenerate_dimension,
    "MDL-BRIDGE-009": classify_bridge_table,
    "MDL-AUX-010": classify_auxiliary_table,
    "MDL-PARAM-011": classify_parameter_table,
    "MDL-FLAT-012": classify_flat_table,
    "MDL-MIXED-013": classify_mixed_table,
    "MDL-ATTRREP-014": classify_repeated_attributes,
    "MDL-MEASURE-015": classify_stored_measures,
    "MDL-DIMEXTRACT-016": classify_extractable_dimension,
}
