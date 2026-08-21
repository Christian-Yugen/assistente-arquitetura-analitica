"""Registro separado de classificadores semânticos autorizados."""

from engine.semantic.date_generic import classify_date_generic
from engine.semantic.identifier import classify_identifier
from engine.semantic.percentage import classify_percentage
from engine.semantic.quantity import classify_quantity

SEMANTIC_RULE_IMPLEMENTATIONS = {
    "SEM-DATE-001": classify_date_generic,
    "SEM-ID-003": classify_identifier,
    "SEM-QTY-005": classify_quantity,
    "SEM-PCT-007": classify_percentage,
}
