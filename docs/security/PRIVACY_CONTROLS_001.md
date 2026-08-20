# PRIVACY-CONTROLS-001 — Controles Implementados no MVP Draft

**Status:** controles de proteção em vigor para o escopo implementado.  
**Limite:** a exclusão física do objeto em armazenamento permanece bloqueada até a disponibilização de uma operação oficial de deleção.

O MVP processa workbooks exclusivamente no servidor e adota minimização de dados antes da persistência. O diagnóstico estruturado permanece limitado ao contrato canônico draft, e o arquivo não é disponibilizado em consultas de histórico depois de concluída a análise.

| Camada | Controle aplicado | Evidência automatizada |
|---|---|---|
| Entrada | Extensão `.xlsx`, MIME permitido, base64, assinatura ZIP, nome seguro e limite de 25 MB. | `server/analysisPipeline.test.ts` |
| Pré-persistência | Inspeção Python do workbook antes de `storagePut`, com limite máximo de 10 abas. | `server/analysisPipeline.test.ts` e testes do motor |
| Minimização | Profiler produz contexto agregado e não preserva valores brutos; títulos de abas são anonimizados. | `engine/tests/test_workbook_profiling.py` |
| Sanitização | CPF, e-mail, nomes explicitamente rotulados e nomes de arquivo são mascarados em metadados, projeto e entrada do motor. | `server/analysisPipeline.test.ts` e `server/analysisRouter.flow.test.ts` |
| Diagnóstico | Payload com conteúdo sensível detectável ou título de aba não anonimizado é bloqueado antes de `createAnalysisDiagnostic`. | `server/analysisRouter.flow.test.ts` |
| Erros | Falhas internas são convertidas em mensagem genérica para o cliente. | `server/analysisRouter.flow.test.ts` |
| Retenção | A referência privada é removida ao final, com `storageKey: null`, `retentionStatus: "reference_removed"` e data de auditoria owner-scoped. | `server/analysisRouter.flow.test.ts`, `server/db.writeScope.test.ts` e `server/analysisRetention.test.ts` |

> A remoção da referência no banco reduz a superfície de acesso operacional, mas não equivale à exclusão física no provedor de armazenamento. Enquanto a operação oficial não existir, esse limite permanece documentado e bloqueia qualquer alegação de retenção definitiva.

Os logs de fluxo não incluem conteúdo de workbook nem detalhes de exceção do motor retornados ao cliente. A implementação não realiza inferência ou enriquecimento semântico por LLM no modo draft atual.
