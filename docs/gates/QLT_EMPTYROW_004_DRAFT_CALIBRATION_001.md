# QLT-EMPTYROW-004 — Gate de Calibração Draft

**Gate:** `QLT-EMPTYROW-004-DRAFT-CALIBRATION-001`  
**Regra:** `QLT-EMPTYROW-004` — Linhas vazias  
**Versão executável:** `0.1.0-reconstructed.1`  
**Decisão:** aprovada para ativação exclusiva no perfil draft.  
**Produção:** bloqueada.

## Fundamento de autorização

O gate de reconstrução `QLT-EMPTYROW-004-RECONSTRUCTION-001` registra a decisão de Chris pela opção A: considerar somente blocos de linhas inteiramente vazias entre linhas com conteúdo, manter sua exclusão dos demais cálculos e não modificar a planilha. O presente gate só promove a implementação local após a evidência técnica abaixo; não cria uma nova interpretação de negócio.

| Controle revisado | Evidência |
|---|---|
| Política e especificação | `QLT_EMPTYROW_004_POLICY_RECONSTRUCTED_001.md` e `QLT_EMPTYROW_004_LOGICAL_SPEC_RECONSTRUCTED_001.md` |
| Perfil privado | `EmptyRowsProfile`, sem conteúdo, título bruto ou posição de célula |
| Golden dataset | `GD-QLT-EMPTYROW-004-001`, somente métricas agregadas |
| Integridade | SHA-256 `4884794020cc5a98e2c0e94ac62956a3baeb239a209fc91f39aa06945bed86e9` |
| Calibração | `CAL-QLT-EMPTYROW-004-001`: 3 TP, 0 FP, 0 FN |
| Testes | Perfil, exclusões, severidade, pergunta de alta severidade, contrato, privacidade e regressão golden |

> A calibração cobre cenários sintéticos agregados de baixa, média e alta proporção, além de exclusões sem linhas vazias internas ou sem linhas com conteúdo. Ela não comprova desempenho em dados de produção.

## Limites da ativação

A allowlist pode conter somente `QLT-EMPTYROW-004: QLT-EMPTYROW-004-DRAFT-CALIBRATION-001`. A regra emite, no máximo, um finding por aba e não revela valores, números de linha, títulos brutos, fórmulas ou amostras. Ela não exclui, move, preenche ou consolida linhas; tampouco infere chaves, granularidade, subtotais ou significado de separadores.

Esta aprovação não remove os bloqueios de produção do Gate MVP 1.0, incluindo catálogo incompleto, calibração limitada a sintéticos, exclusão física de armazenamento pendente, E2E integral pendente e recuperação canônica da QLT-NULL-001.
