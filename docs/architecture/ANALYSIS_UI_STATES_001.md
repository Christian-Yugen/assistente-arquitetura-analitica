# ANALYSIS-UI-STATES-001 — Evidência dos Estados do Workspace

**Status:** aprovado para o MVP draft.  
**Escopo:** interface do procedimento autenticado `analysis.analyzeWorkbook`.

O workspace deriva o estado apresentado ao usuário em `client/src/lib/analysisUiState.ts` e o consome em `client/src/pages/Home.tsx`. Os avisos de autenticação, o controle de submissão e a confirmação de resultado foram extraídos para `client/src/components/AnalysisFlowState.tsx`, evitando que a cobertura automatizada dependa de lógica visual duplicada.

| Estado | Condição de origem | Evidência exibida | Tratamento de interação |
|---|---|---|---|
| `auth_loading` | Consulta de sessão ainda carregando | Mensagem de verificação da sessão segura | O formulário não é apresentado. |
| `sign_in_required` | Sessão ausente | Contexto de isolamento de projetos e botão de entrada | O botão inicia o fluxo oficial de login. |
| `auth_error` | Falha ao consultar a sessão | Mensagem de indisponibilidade e nova tentativa | O botão reinicia o fluxo oficial de login. |
| `ready` | Sessão válida e mutation inativa | Formulário de envio do workbook | A submissão permanece disponível. |
| `analyzing` | Mutation `analysis.analyzeWorkbook` pendente | Rótulo “Analisando estrutura…” | O botão de submissão recebe o atributo `disabled`. |
| `success` | Mutation concluída com diagnóstico persistido | Confirmação da versão criada e ação “Ver diagnóstico” | A navegação desloca para a lista de versões. |

A suíte em `client/src/components/AnalysisFlowState.test.tsx` renderiza os componentes reais no servidor e verifica os estados de autenticação, a presença da ação de login, o bloqueio do botão pendente e a confirmação de sucesso. A suíte integrada em `client/src/pages/Home.test.tsx` usa mocks controlados de autenticação e tRPC para validar a composição efetiva do workspace. Por fim, `client/src/pages/Home.interaction.test.tsx` executa a ação “Ver diagnóstico” em DOM e comprova o deslocamento suave até `#versoes`. A suíte da função pura, em `client/src/lib/analysisUiState.test.ts`, mantém a cobertura das condições de derivação. A configuração em `vitest.config.ts` inclui explicitamente arquivos de teste `.tsx`.
