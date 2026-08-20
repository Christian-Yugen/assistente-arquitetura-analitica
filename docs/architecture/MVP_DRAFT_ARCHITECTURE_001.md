# MVP-DRAFT-ARCHITECTURE-001 — Arquitetura do Assistente de Arquitetura Analítica

**Estado:** implementado para análise de qualidade no perfil draft.  
**Decisão de ambiente:** o motor Python é executado exclusivamente no servidor; o navegador não recebe workbook bruto nem executa regras.

O MVP recebe uma planilha `.xlsx`, aplica controles de entrada antes de persistência, executa o motor determinístico em processo Python isolado, grava o diagnóstico canônico e expõe o resultado apenas ao mesmo proprietário autenticado. A arquitetura separa transporte, orquestração, processamento analítico, persistência e apresentação para que o diagnóstico não dependa de regras de interface ou de inferência livre.

| Camada | Responsabilidade | Evidência de implementação |
|---|---|---|
| Cliente React | Autenticação, seleção do arquivo, estado de processamento, histórico e exportação JSON. | `client/src/pages/Home.tsx`, `client/src/components/AnalysisFlowState.tsx` |
| API tRPC | Aplica autenticação, valida a entrada, orquestra a análise e converte falhas em respostas seguras. | `server/routers.ts` |
| Validação pré-persistência | Valida extensão, MIME, base64, assinatura ZIP, tamanho, legibilidade real e máximo de abas. | `server/analysisPipeline.ts`, `engine/workbook_validator.py` |
| Motor Python | Faz profiling agregado, executa regras autorizadas e valida o diagnóstico contra o contrato. | `engine/workbook_runner.py`, `engine/pipeline/quality_diagnosis.py` |
| Persistência | Armazena metadados, versões e payload canônico com filtro obrigatório por proprietário. | `drizzle/schema.ts`, `server/db.ts` |
| Armazenamento privado | Mantém o objeto durante a execução e remove sua referência após a análise. | `server/storage.ts`, `server/routers.ts` |

## Fluxo de análise

O procedimento `analysis.analyzeWorkbook` recebe metadados e base64 no canal autenticado. `validateWorkbookUpload` filtra condições superficiais do arquivo; em seguida, `inspectWorkbookBeforePersistence` escreve o conteúdo em diretório temporário e chama `engine.workbook_validator`. Esse validador abre o arquivo com `openpyxl` em modo de leitura e rejeita um ZIP que não seja workbook XLSX válido. Somente depois da inspeção a referência privada é criada no armazenamento.

O `engine.workbook_runner` abre o workbook para profiling e entrega ao executor apenas estatísticas agregadas por coluna. O executor chama exclusivamente as regras presentes na allowlist do perfil draft, produz findings, perguntas e recomendações derivadas das regras, valida o contrato e devolve JSON. O servidor bloqueia o payload se detectar conteúdo sensível, grava a versão do diagnóstico no escopo do proprietário e remove `storageKey` da referência de arquivo ao final.

> O arquivo de origem é uma entrada operacional transitória. O diagnóstico persistido contém evidências agregadas, identificadores e textos sanitizados; ele não deve conter valores de células, CPF, e-mail, nome explicitamente rotulado ou título de aba não anonimizado.

## Fronteiras e limitações

O perfil vigente é deliberadamente parcial. Ele executa `QLT-NUMTEXT-007` e `QLT-NULL-001`; as outras regras do catálogo de 95 regras não são chamadas pelo executor sem intake, especificação e gate. O bloco `proposed_model` usa apenas marcadores governados para insuficiência de evidência, portanto não é uma proposta automática de fatos, dimensões, relacionamentos ou métricas.

A remoção de referência no banco não equivale a exclusão física no provedor de armazenamento. A limitação está registrada na `RETENTION-EXCEPTION-001`, aceita para o MVP draft e incompatível com alegação de prontidão para produção. Consulte [PRIVACY-CONTROLS-001](../security/PRIVACY_CONTROLS_001.md) para controles compensatórios e critérios de reavaliação.
