from engine.alerts.sensitivity import classify_sensitive_data_processing_restriction


ALERT_RULE_IMPLEMENTATIONS = {
    "ALT-SENS-001": classify_sensitive_data_processing_restriction,
}
