"""Registro explícito de implementações de regras de qualidade disponíveis no motor."""

from .numtext import NumericTextColumnProfile, evaluate_numeric_text


QUALITY_RULE_IMPLEMENTATIONS = {
    "QLT-NUMTEXT-007": evaluate_numeric_text,
}

__all__ = ["NumericTextColumnProfile", "QUALITY_RULE_IMPLEMENTATIONS"]
