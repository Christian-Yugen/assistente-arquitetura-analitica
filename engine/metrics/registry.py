from engine.metrics.completion import classify_completion_rate_concept
from engine.metrics.sum import classify_sum_concept
from engine.metrics.count import classify_count_concept
from engine.metrics.distinct_count import classify_distinct_count_concept
from engine.metrics.average import classify_average_concept
from engine.metrics.minmax import classify_minmax_concept
from engine.metrics.rate import classify_rate_concept
from engine.metrics.absolute_delta import classify_absolute_delta_concept
from engine.metrics.percentage_delta import classify_percentage_delta_concept
from engine.metrics.running_total import classify_running_total_concept
from engine.metrics.weighted_average import classify_weighted_average_concept
from engine.metrics.semiadditive import classify_semiadditive_concept
from engine.metrics.domain import classify_domain_metric_concept


METRIC_RULE_IMPLEMENTATIONS = {
    "MET-COMPL-001": classify_completion_rate_concept,
    "MET-SUM-002": classify_sum_concept,
    "MET-COUNT-003": classify_count_concept,
    "MET-DCOUNT-004": classify_distinct_count_concept,
    "MET-AVG-005": classify_average_concept,
    "MET-MINMAX-006": classify_minmax_concept,
    "MET-RATE-007": classify_rate_concept,
    "MET-ABSDELTA-008": classify_absolute_delta_concept,
    "MET-PCTDELTA-009": classify_percentage_delta_concept,
    "MET-RUNNING-010": classify_running_total_concept,
    "MET-WAVG-011": classify_weighted_average_concept,
    "MET-SEMIADD-012": classify_semiadditive_concept,
    "MET-DOMAIN-013": classify_domain_metric_concept,
}
