from engine.metrics.completion import classify_completion_rate_concept
from engine.metrics.sum import classify_sum_concept
from engine.metrics.count import classify_count_concept
from engine.metrics.distinct_count import classify_distinct_count_concept
from engine.metrics.average import classify_average_concept
from engine.metrics.minmax import classify_minmax_concept


METRIC_RULE_IMPLEMENTATIONS = {
    "MET-COMPL-001": classify_completion_rate_concept,
    "MET-SUM-002": classify_sum_concept,
    "MET-COUNT-003": classify_count_concept,
    "MET-DCOUNT-004": classify_distinct_count_concept,
    "MET-AVG-005": classify_average_concept,
    "MET-MINMAX-006": classify_minmax_concept,
}
