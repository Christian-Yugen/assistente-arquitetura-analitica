"""Registro explícito de implementações de regras de qualidade disponíveis no motor."""

from .numtext import NumericTextColumnProfile, evaluate_numeric_text
from .nulls import NullColumnProfile, evaluate_nulls
from .catvar import CategoricalVariationColumnProfile, evaluate_categorical_variations
from .duplicates import DuplicateRowsSheetProfile, evaluate_duplicate_rows
from .empty_columns import EmptyColumnProfile, evaluate_empty_column
from .empty_rows import EmptyRowsSheetProfile, evaluate_empty_rows


QUALITY_RULE_IMPLEMENTATIONS = {
    "QLT-NUMTEXT-007": evaluate_numeric_text,
    "QLT-NULL-001": evaluate_nulls,
    "QLT-CATVAR-008": evaluate_categorical_variations,
    "QLT-DUP-002": evaluate_duplicate_rows,
    "QLT-EMPTYCOL-003": evaluate_empty_column,
    "QLT-EMPTYROW-004": evaluate_empty_rows,
}

__all__ = ["NumericTextColumnProfile", "NullColumnProfile", "CategoricalVariationColumnProfile", "DuplicateRowsSheetProfile", "EmptyColumnProfile", "EmptyRowsSheetProfile", "QUALITY_RULE_IMPLEMENTATIONS"]
