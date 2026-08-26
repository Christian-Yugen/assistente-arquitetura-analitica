# Reconciliação de Linhagem para Produção — 001

**Estado:** inventário documental; não autoriza produção. **Escopo:** as 95 regras `executable_draft` do índice governado.

## Decisão de autoridade

O índice `rule-implementation-readiness-v1.json` é a fonte operacional de executabilidade draft e registra **95 regras `executable_draft`** e **zero `intake_required`**. Esse dado não substitui os gates individuais, a allowlist do catálogo, a calibração draft, os testes ou as restrições de produção.

## Inventário de linhagem

A auditoria de formato dos 95 IDs executáveis encontrou nove IDs sem arquivo de intake individual, dez intakes em formato legado sem `local_readiness`, quinze intakes em formato atual ainda rotulados `intake_required` e sessenta e uma entradas com `local_readiness=executable_draft` sem o campo booleano histórico `execution_blocked`. Essas diferenças são de **linhagem e esquema documental**; elas não alteram a allowlist do motor nem promovem qualquer regra.

| Grupo | Quantidade | IDs ou tratamento | Decisão atual |
|---|---:|---|---|
| Sem intake individual | 9 | `QLT-NULL-001`, `QLT-DUP-002`, `QLT-EMPTYCOL-003`, `QLT-EMPTYROW-004`, `QLT-MIXTYPE-005`, `QLT-BADDATE-006`, `QLT-NUMTEXT-007`, `QLT-WHITESPACE-009`, `QLT-TOTALROW-010` | Preservar os gates e evidências existentes; exigir mapa de migração documental antes de promoção. |
| Intake legado | 10 | `SEM-QTY-005`, `SEM-CURR-006`, `SEM-PCT-007`, `SEM-TARGET-013`, `SEM-ACTUAL-014`, `SEM-SENS-015`, `MDL-FACTPER-001`, `MDL-FACTTXN-002`, `MDL-DIMSTD-004`, `MDL-DIMCAL-006` | Normalizar somente em ciclo próprio, sem alterar comportamento do motor. |
| Intake com prontidão documental defasada | 15 | `QLT-CATVAR-008`, `QLT-NEGATIVE-011`, `QLT-OUTLIER-012`, `QLT-FORMULA-013`, `QLT-HEADERS-014`, `QLT-IDMISS-015`, `SEM-DATE-001`, `SEM-ID-003`, `GRN-COMP-001`, `MET-DAX-015`, `ALT-METRIC-006`, `ALT-SUMPCT-007`, `ALT-AVGAVG-008`, `ALT-MIXGRAIN-009`, `ALT-LOWCONF-010` | Reconciliar os registros com evidência de gate já existente, sem promover produção. |

## Bloqueios produtivos independentes

| Bloqueio | Estado | Condição para reavaliação |
|---|---|---|
| Exclusão física do objeto privado | Bloqueado; somente remoção de referência foi implementada. | Operação de armazenamento suportada, teste owner-scoped e gate específico. |
| Calibração para produção | Bloqueada; goldens são estritamente sintéticos e limitados ao draft. | Conjuntos aprovados, métricas FP/FN por regra e decisão humana formal. |
| Testes ponta a ponta | Bloqueados para produção. | Cenário automatizado em ambiente provisionado sem dados pessoais e isolamento comprovado. |
| Linhagem canônica da QLT-NULL-001 | Reconstrução autorizada, sem recuperação da fonte original. | Recuperação ou substituição formal da fonte e decisão de promoção correspondente. |
| Reconciliação de intakes | Pendente. | Mapa versionado de migração de esquema e validação contra allowlist/gates sem alterar runtime. |

> A cobertura de **95/95** regras draft é um marco de catálogo, não um gate produtivo. Nenhuma regra, finding ou recomendação passa a operar em produção por este documento. Os sinais independentes que não possuem fonte autorizada continuam fixados em zero e fail-closed.

## Próximo gate permitido

O próximo ciclo permitido é **documental**: propor o mapa de migração de linhagem dos intakes e o contrato canônico de prova de executabilidade. Qualquer script de migração, alteração de runtime, calibração produtiva, exclusão física, execução E2E em ambiente provisionado ou promoção de ambiente requer autorização explícita de Chris e gate próprio.
