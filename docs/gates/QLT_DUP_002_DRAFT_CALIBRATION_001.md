# QLT-DUP-002-DRAFT-CALIBRATION-001

**Data:** 20 de agosto de 2026.
**Decisão:** aprovada exclusivamente para execução no perfil draft.

## Evidências revisadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política reconstruída | `QLT_DUP_002_POLICY_RECONSTRUCTED_001.md` | Aprovada na alternativa A por Chris |
| Escopo | Linhas integralmente idênticas dentro de uma aba | Conforme |
| Inferência de chaves | Ausente por projeto e por teste | Conforme |
| Privacidade | Perfil, finding e fixture sem valores, assinaturas ou índices de linha | Conforme |
| Golden dataset | `GD-QLT-DUP-002-001`, manifesto SHA-256 `bdc454e5cec0de26bffc440e0a9922bbc2646c7baa1568a0f5fce4f8a7db92ab` | Conforme |
| Calibração | `CAL-QLT-DUP-002-001`: 5 TP, 0 FP, 0 FN | Conforme no escopo sintético agregado |

## Limites da autorização

> A ativação permite somente identificar candidatos de linhas integralmente repetidas no diagnóstico draft. Ela não autoriza exclusão, retenção, mesclagem, deduplicação, comparação entre abas, inferência de chave ou promoção produtiva.

A versão executável é `0.1.0-reconstructed.1`. A regra deve usar o gate `QLT-DUP-002-DRAFT-CALIBRATION-001` na allowlist explícita. O Gate MVP 1.0 continua bloqueado pelos pré-requisitos produtivos já documentados.
