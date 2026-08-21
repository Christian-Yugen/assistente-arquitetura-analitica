from __future__ import annotations

from dataclasses import dataclass

from engine.profiling.semantic_identifier import SemanticIdentifierProfile


SEMANTIC_SENSITIVITY_BASIS = "closed_sensitive_header_non_missing1_v1"


@dataclass(frozen=True)
class SemanticSensitivityProfile:
    header_eligible: bool = False
    non_missing_count: int = 0
    basis: str = SEMANTIC_SENSITIVITY_BASIS


def profile_semantic_sensitivity(identifier: SemanticIdentifierProfile) -> SemanticSensitivityProfile:
    """Deriva somente sinais agregados do perfil privado já existente de identificador."""
    return SemanticSensitivityProfile(
        header_eligible=identifier.sensitive_header,
        non_missing_count=identifier.non_missing_count,
    )
