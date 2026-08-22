"""Registro separado de classificadores semânticos autorizados."""

from engine.semantic.date_generic import classify_date_generic
from engine.semantic.competence import classify_competence_date
from engine.semantic.description import classify_name_or_description
from engine.semantic.actual import classify_actual
from engine.semantic.currency import classify_currency
from engine.semantic.identifier import classify_identifier
from engine.semantic.percentage import classify_percentage
from engine.semantic.quantity import classify_quantity
from engine.semantic.sensitivity import classify_sensitivity
from engine.semantic.target import classify_target

SEMANTIC_RULE_IMPLEMENTATIONS = {
    "SEM-DATE-001": classify_date_generic,
    "SEM-COMP-002": classify_competence_date,
    "SEM-DESC-004": classify_name_or_description,
    "SEM-ACTUAL-014": classify_actual,
    "SEM-CURR-006": classify_currency,
    "SEM-ID-003": classify_identifier,
    "SEM-QTY-005": classify_quantity,
    "SEM-SENS-015": classify_sensitivity,
    "SEM-PCT-007": classify_percentage,
    "SEM-TARGET-013": classify_target,
}
