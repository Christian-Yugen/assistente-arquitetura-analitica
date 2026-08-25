from engine.metrics.completion import classify_completion_rate_concept


METRIC_RULE_IMPLEMENTATIONS = {
    "MET-COMPL-001": classify_completion_rate_concept,
}
