"""Registro separado de classificadores semânticos autorizados."""

from engine.semantic.date_generic import classify_date_generic
from engine.semantic.identifier import classify_identifier

SEMANTIC_RULE_IMPLEMENTATIONS = {"SEM-DATE-001": classify_date_generic, "SEM-ID-003": classify_identifier}
