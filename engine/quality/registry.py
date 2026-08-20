"""Registro explícito de implementações de regras de qualidade disponíveis no motor."""

from .numtext import NumericTextColumnProfile, evaluate_numeric_text
from .nulls import NullColumnProfile, evaluate_nulls
from .catvar import CategoricalVariationColumnProfile, evaluate_categorical_variations


QUALITY_RULE_IMPLEMENTATIONS = {
    "QLT-NUMTEXT-007": evaluate_numeric_text,
    "QLT-NULL-001": evaluate_nulls,
    "QLT-CATVAR-008": evaluate_categorical_variations,
}

__all__ = ["NumericTextColumnProfile", "NullColumnProfile", "CategoricalVariationColumnProfile", "QUALITY_RULE_IMPLEMENTATIONS"]
