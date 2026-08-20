# QLT-EMPTYCOL-003-DRAFT-CALIBRATION-001

**Data:** 20 de agosto de 2026.  
**Decisão:** aprovada exclusivamente para execução no perfil draft.

## Evidências revisadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política reconstruída | `QLT_EMPTYCOL_003_POLICY_RECONSTRUCTED_001.md` | Alternativa A aprovada por Chris |
| Escopo | Colunas cujas células observadas são todas nulas ou texto em branco | Conforme |
| Exclusões | `0`, `false`, datas, fórmulas, valores válidos, `NaN` numérico e sentinelas | Conforme por política e teste |
| Privacidade | Perfil, finding e fixture não carregam valores brutos nem posições de células | Conforme |
| Golden dataset | `GD-QLT-EMPTYCOL-003-001`, manifesto SHA-256 `174de4e6de82ae6560af96d5d8495f3bb32653a67c007cf71606a06dccb11f01` | Conforme |
| Calibração | `CAL-QLT-EMPTYCOL-003-001`: 4 TP, 0 FP, 0 FN | Conforme no escopo sintético agregado |

## Limites da autorização

> A ativação permite apenas apontar uma coluna estruturalmente vazia para validação no diagnóstico draft. Ela não autoriza excluir colunas, inferir finalidade, tratar sentinelas como ausências, alterar a planilha nem promover a regra para produção.

A versão executável é `0.1.0-reconstructed.1`. A regra usa o gate `QLT-EMPTYCOL-003-DRAFT-CALIBRATION-001` na allowlist explícita. O Gate MVP 1.0 continua bloqueado pelos pré-requisitos produtivos documentados.
