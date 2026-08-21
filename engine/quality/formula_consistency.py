"""QLT-FORMULA-013: ruptura de presença de fórmula sem ler expressões."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.formula_consistency import (
    FORMULA_CONSISTENCY_BASIS,
    MINIMUM_FORMULA_COUNT,
    MINIMUM_FORMULA_SHARE,
    MINIMUM_PHYSICAL_NONEMPTY_COUNT,
    FormulaConsistencyProfile,
)


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class FormulaConsistencyColumnProfile:
    name: str
    formulas: FormulaConsistencyProfile


class Finding(TypedDict):
    rule_id: str
    category: str
    severity: Severity
    confidence: float
    title: str
    description: str
    impact: str
    recommendation: str
    evidence: list[dict[str, object]]
    question: dict[str, object] | None


def _is_applicable(profile: FormulaConsistencyColumnProfile) -> bool:
    formulas = profile.formulas
    if (
        not formulas.eligible
        or formulas.basis != FORMULA_CONSISTENCY_BASIS
        or formulas.physical_nonempty_count < MINIMUM_PHYSICAL_NONEMPTY_COUNT
        or formulas.formula_count < MINIMUM_FORMULA_COUNT
        or formulas.formula_count > formulas.physical_nonempty_count
        or formulas.nonformula_count != formulas.physical_nonempty_count - formulas.formula_count
        or formulas.nonformula_count <= 0
        or formulas.nonformula_count > formulas.physical_nonempty_count
    ):
        return False
    if formulas.formula_count / formulas.physical_nonempty_count < MINIMUM_FORMULA_SHARE:
        return False
    return formulas.nonformula_ratio == round(formulas.nonformula_count / formulas.physical_nonempty_count, 8)


def _severity(ratio: float) -> Severity:
    if ratio <= 0.05:
        return "low"
    if ratio <= 0.10:
        return "medium"
    return "high"


def _question(severity: Severity) -> dict[str, object]:
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": False,
        "text": "As substituições manuais detectadas em uma coluna predominantemente calculada foram intencionais ou a coluna deveria manter um cálculo consistente?",
        "reason": "A presença ou ausência de fórmula é determinística, mas a intenção do valor manual exige confirmação humana e contexto de negócio.",
        "options": [
            {"option_id": "intentional_override", "label": "As substituições manuais são intencionais e documentadas."},
            {"option_id": "possible_formula_gap", "label": "Há possível lacuna de fórmula que precisa de verificação na origem."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "metrics", "report"],
    }


def evaluate_formula_consistency(profile: FormulaConsistencyColumnProfile) -> list[Finding]:
    """Emite finding agregado; não lê, compara, copia ou corrige fórmulas."""

    if not _is_applicable(profile):
        return []
    formulas = profile.formulas
    severity = _severity(formulas.nonformula_ratio)
    copy = {
        "low": ("Ruptura pontual de cálculo para validação", "Uma substituição manual pode exigir confirmação antes de métricas e inferências."),
        "medium": ("Rupturas recorrentes de cálculo para validação", "Substituições manuais recorrentes podem afetar agregações e interpretação analítica."),
        "high": ("Muitas rupturas de cálculo para validação", "A coluna deve ser validada antes de sustentar inferências analíticas ou recomendações."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-FORMULA-NONFORMULA-COUNT", "effect": "negative", "observed_value": formulas.nonformula_count, "expected_condition": "nonformula_count = 0"},
        {"code": "EVD-FORMULA-NONFORMULA-RATIO", "effect": "negative", "observed_ratio": formulas.nonformula_ratio, "expected_condition": "nonformula_ratio = 0"},
        {"code": "EVD-FORMULA-COUNT", "effect": "technical", "observed_value": formulas.formula_count, "expected_condition": "formula_count >= 8"},
        {"code": "EVD-FORMULA-PHYSICAL-BASE", "effect": "technical", "observed_value": formulas.physical_nonempty_count, "expected_condition": "physical_nonempty_count >= 10"},
        {"code": "EVD-FORMULA-BASIS", "effect": "technical", "observed_value": formulas.basis, "expected_condition": FORMULA_CONSISTENCY_BASIS},
    ]
    return [{
        "rule_id": "QLT-FORMULA-013",
        "category": "quality",
        "severity": severity,
        "confidence": 0.85,
        "title": copy[0],
        "description": f"Foram identificadas {formulas.nonformula_count} substituições manuais ({formulas.nonformula_ratio * 100:.1f}% da base física elegível) em coluna predominantemente calculada.",
        "impact": copy[1],
        "recommendation": "Validar com o responsável de negócio se as substituições manuais são intencionais antes de definir métricas, agregações ou qualquer tratamento fora desta análise.",
        "evidence": evidence,
        "question": _question(severity),
    }]
