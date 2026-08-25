from engine.alerts.sensitivity import classify_sensitive_data_processing_restriction
from engine.alerts.quality import classify_critical_quality_risk


ALERT_RULE_IMPLEMENTATIONS = {
    "ALT-SENS-001": classify_sensitive_data_processing_restriction,
    "ALT-QUALITY-002": classify_critical_quality_risk,
}
