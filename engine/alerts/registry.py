from engine.alerts.sensitivity import classify_sensitive_data_processing_restriction
from engine.alerts.quality import classify_critical_quality_risk
from engine.alerts.grain import classify_undefined_grain_modeling_block
from engine.alerts.key import classify_invalid_key_modeling_block


ALERT_RULE_IMPLEMENTATIONS = {
    "ALT-SENS-001": classify_sensitive_data_processing_restriction,
    "ALT-QUALITY-002": classify_critical_quality_risk,
    "ALT-GRAIN-003": classify_undefined_grain_modeling_block,
    "ALT-KEY-004": classify_invalid_key_modeling_block,
}
