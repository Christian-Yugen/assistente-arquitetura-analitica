# Contrato de Reconciliação de Linhagem dos Intakes — 001

**Estado:** documental, aditivo e não executável. **Versão do registro:** `intake-lineage-reconciliation-v1.json`. **Produção:** bloqueada.

## Invariantes obrigatórios

O registro de reconciliação é uma camada de prova documental e não é uma fonte de execução. Ele não pode modificar `DRAFT_RULE_AUTHORIZATIONS`, `RULE_VERSIONS`, registros de implementação, pipeline, contagem do índice, intakes históricos, golden datasets, calibração ou qualquer ambiente. O índice de prontidão permanece a fonte operacional draft; os intakes históricos e seus gates permanecem imutáveis neste ciclo.

## Estrutura mínima de uma ficha

Cada ficha contém `group_id`, `lineage_status`, `rule_ids`, `evidence_scope`, `required_future_action`, `runtime_change_prohibited`, `allowlist_change_prohibited` e `production_authorized`. Ela somente agrupa diferenças de linhagem já auditadas; não infere autorização, não substitui gate e não confirma regra para produção.

| Ficha | Significado | Regras incluídas | Tratamento permitido |
|---|---|---:|---|
| `missing_intake_file` | A regra possui evidências draft no índice e artefatos históricos, mas não um intake individual no formato atual. | 9 | Referenciar a ausência e planejar uma ficha aditiva futura. |
| `legacy_intake_schema` | O intake existe em formato histórico sem `local_readiness`. | 10 | Mapear equivalência documental sem alterar o arquivo original. |
| `stale_intake_readiness` | O intake atual ainda registra prontidão anterior ao estado do índice. | 15 | Registrar reconciliação aditiva para evidência existente, sem mudar execução. |

## Critérios de bloqueio

Toda ficha deve manter `runtime_change_prohibited=true`, `allowlist_change_prohibited=true` e `production_authorized=false`. Qualquer alteração de runtime, migração automatizada, atualização do intake histórico, recalibração produtiva, exclusão física, E2E provisionado ou promoção de ambiente exige novo gate e autorização explícita de Chris.
