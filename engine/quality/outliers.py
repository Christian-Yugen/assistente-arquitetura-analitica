"""QLT-OUTLIER-012: sinaliza extremos Tukey como hipótese de validação humana."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

from engine.profiling.outliers import MINIMUM_PHYSICAL_NUMERIC_COUNT, OUTLIER_BASIS, OutlierProfile


Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class OutlierColumnProfile:
    name: str
    outliers: OutlierProfile


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


def _is_applicable(profile: OutlierColumnProfile) -> bool:
    outliers = profile.outliers
    if (
        not outliers.eligible
        or outliers.basis != OUTLIER_BASIS
        or outliers.physical_numeric_count < MINIMUM_PHYSICAL_NUMERIC_COUNT
        or outliers.physical_nonempty_count < outliers.physical_numeric_count
        or outliers.lower_outlier_count < 0
        or outliers.upper_outlier_count < 0
        or outliers.outlier_count != outliers.lower_outlier_count + outliers.upper_outlier_count
        or outliers.outlier_count <= 0
        or outliers.outlier_count > outliers.physical_numeric_count
    ):
        return False
    if outliers.physical_numeric_count / outliers.physical_nonempty_count < 0.8:
        return False
    return outliers.outlier_ratio == round(outliers.outlier_count / outliers.physical_numeric_count, 8)


def _severity(ratio: float) -> Severity:
    if ratio <= 0.05:
        return "low"
    if ratio <= 0.20:
        return "medium"
    return "high"


def _question(severity: Severity) -> dict[str, object]:
    return {
        "question_type": "single_choice",
        "priority": "high" if severity == "high" else "medium",
        "blocking": False,
        "text": "Os extremos estatísticos identificados representam casos legítimos, erro de digitação, mudança de unidade, exceções operacionais ou um recorte de período que precisa ser validado?",
        "reason": "O método estatístico é determinístico, mas a causa e a relevância de um extremo dependem de confirmação humana e de contexto de negócio.",
        "options": [
            {"option_id": "legitimate_extreme", "label": "Representam casos legítimos ou uma distribuição esperada."},
            {"option_id": "source_issue", "label": "Representam possível problema de origem ou unidade e precisam de verificação externa."},
            {"option_id": "unknown", "label": "Ainda não é possível confirmar."},
        ],
        "affected_modules": ["quality", "semantic_types", "metrics", "report"],
    }


def evaluate_outliers(profile: OutlierColumnProfile) -> list[Finding]:
    """Emite apenas finding agregado; extremos não são corrigidos automaticamente."""

    if not _is_applicable(profile):
        return []
    outliers = profile.outliers
    severity = _severity(outliers.outlier_ratio)
    copy = {
        "low": ("Extremo estatístico para validação", "Um extremo estatístico pode exigir contexto antes de métricas e inferências."),
        "medium": ("Extremos estatísticos recorrentes para validação", "A recorrência dos extremos pode afetar agregações e interpretação analítica."),
        "high": ("Muitos extremos estatísticos para validação", "A coluna deve ser validada antes de sustentar inferências analíticas ou recomendações."),
    }[severity]
    evidence: list[dict[str, object]] = [
        {"code": "EVD-OUTLIER-COUNT", "effect": "negative", "observed_value": outliers.outlier_count, "expected_condition": "outlier_count = 0"},
        {"code": "EVD-OUTLIER-RATIO", "effect": "negative", "observed_ratio": outliers.outlier_ratio, "expected_condition": "outlier_ratio = 0"},
        {"code": "EVD-OUTLIER-LOWER-COUNT", "effect": "technical", "observed_value": outliers.lower_outlier_count, "expected_condition": "lower_outlier_count >= 0"},
        {"code": "EVD-OUTLIER-UPPER-COUNT", "effect": "technical", "observed_value": outliers.upper_outlier_count, "expected_condition": "upper_outlier_count >= 0"},
        {"code": "EVD-OUTLIER-PHYSICAL-BASE", "effect": "technical", "observed_value": outliers.physical_numeric_count, "expected_condition": "physical_numeric_count >= 20"},
        {"code": "EVD-OUTLIER-BASIS", "effect": "technical", "observed_value": outliers.basis, "expected_condition": OUTLIER_BASIS},
    ]
    return [{
        "rule_id": "QLT-OUTLIER-012",
        "category": "quality",
        "severity": severity,
        "confidence": 0.85,
        "title": copy[0],
        "description": f"Foram identificados {outliers.outlier_count} extremos estatísticos ({outliers.outlier_ratio * 100:.1f}% da base numérica elegível).",
        "impact": copy[1],
        "recommendation": "Validar com o responsável de negócio os extremos identificados antes de definir métricas, agregações ou qualquer tratamento fora desta análise.",
        "evidence": evidence,
        "question": _question(severity),
    }]
