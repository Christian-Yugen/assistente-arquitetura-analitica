# OWNER-SCOPE-PROOF-001 — Isolamento de Leituras Analíticas

**Status:** aprovado para cobertura estruturada do MVP draft.  
**Limite explícito:** a prova de persistência contra um banco provisionado continua pendente.

As leituras analíticas em `server/db.ts` recebem `ownerId` obrigatório e aplicam esse escopo ao recuperar projetos, diagnósticos, versões e dados exibidos no histórico. A evidência automatizada está em `server/db.ownerScope.test.ts`. Ela utiliza um banco estruturado simulado para executar os helpers reais, preservando a construção dos predicados de consulta e sem acessar dados externos.

| Helper verificado | Cenário de isolamento | Resultado comprovado |
|---|---|---|
| `listAnalysisProjectsForOwner` | Um diagnóstico de outro proprietário usa o mesmo `projectId` e uma versão superior. | A listagem retorna somente o projeto próprio e conserva a última versão do mesmo proprietário. |
| `getAnalysisDiagnosticForOwner` | O identificador de diagnóstico pertence a outro proprietário. | A consulta retorna ausência de recurso. |
| `getAnalysisProjectForOwner` | O identificador de projeto pertence a outro proprietário. | A consulta retorna ausência de recurso. |
| `getNextDiagnosticVersion` | Há diagnóstico externo com versão numericamente superior no mesmo projeto. | A próxima versão é calculada apenas a partir dos diagnósticos do proprietário correto. |

O teste também afirma que cada predicado executado contém o vínculo com `ownerId`. Essa prova complementa, mas não substitui, a validação integrada com banco provisionado prevista no item de backlog de persistência real.
