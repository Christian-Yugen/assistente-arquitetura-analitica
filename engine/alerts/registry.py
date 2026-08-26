from engine.alerts.sensitivity import classify_sensitive_data_processing_restriction
from engine.alerts.quality import classify_critical_quality_risk
from engine.alerts.grain import classify_undefined_grain_modeling_block
from engine.alerts.key import classify_invalid_key_modeling_block
from engine.alerts.ambiguity import classify_structural_ambiguity_modeling_block
from engine.alerts.metric_risk import classify_potentially_misleading_metric_review
from engine.alerts.percentage_sum import classify_percentage_sum_review
from engine.alerts.average_of_averages import classify_average_of_averages_review
from engine.alerts.mixed_grain import classify_mixed_grain_review
from engine.alerts.low_confidence import classify_low_confidence_review
from engine.alerts.snapshot_grain import classify_snapshot_grain
from engine.alerts.period_per_row import classify_period_per_row
from engine.alerts.entity_association import classify_entity_association
from engine.alerts.pre_aggregation import classify_pre_aggregation
from engine.alerts.inconsistent_grain import classify_inconsistent_grain


ALERT_RULE_IMPLEMENTATIONS = {
    "ALT-SENS-001": classify_sensitive_data_processing_restriction,
    "ALT-QUALITY-002": classify_critical_quality_risk,
    "ALT-GRAIN-003": classify_undefined_grain_modeling_block,
    "ALT-KEY-004": classify_invalid_key_modeling_block,
    "ALT-AMBIG-005": classify_structural_ambiguity_modeling_block,
    "ALT-METRIC-006": classify_potentially_misleading_metric_review,
    "ALT-SUMPCT-007": classify_percentage_sum_review,
    "ALT-AVGAVG-008": classify_average_of_averages_review,
    "ALT-MIXGRAIN-009": classify_mixed_grain_review,
    "ALT-LOWCONF-010": classify_low_confidence_review,
    "GRN-SNAP-006": classify_snapshot_grain,
    "GRN-PERIOD-005": classify_period_per_row,
    "GRN-ASSOC-007": classify_entity_association,
    "GRN-PREAGG-008": classify_pre_aggregation,
    "GRN-INCONS-009": classify_inconsistent_grain,
}
