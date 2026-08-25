from engine.metrics.completion import classify_completion_rate_concept
from engine.metrics.sum import classify_sum_concept
from engine.metrics.count import classify_count_concept


METRIC_RULE_IMPLEMENTATIONS = {
    "MET-COMPL-001": classify_completion_rate_concept,
    "MET-SUM-002": classify_sum_concept,
    "MET-COUNT-003": classify_count_concept,
}
