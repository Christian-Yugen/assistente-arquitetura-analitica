"""Registro separado de classificadores semânticos autorizados."""

from engine.semantic.date_generic import classify_date_generic

SEMANTIC_RULE_IMPLEMENTATIONS = {"SEM-DATE-001": classify_date_generic}
