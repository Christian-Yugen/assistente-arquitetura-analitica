# ANALYSIS-PROCESSING-STATE-001 — Estado de Processamento do Workspace

**Status:** implementado e validado para o MVP draft.  
**Modelo de execução:** mutation síncrona `analysis.analyzeWorkbook`.

Quando a mutation está pendente, o workspace exibe um painel acessível com `role="status"` e `aria-live="polite"`. O painel informa que a análise ocorre no servidor, identifica o workbook selecionado e descreve qualitativamente as proteções do fluxo: validação, isolamento, profiling e diagnóstico.

> O MVP não apresenta percentual, tempo estimado ou etapas concluídas, porque o procedimento atual não fornece eventos intermediários observáveis. Exibir progresso numérico nessa condição seria uma simulação enganosa.

| Elemento | Comportamento pendente |
|---|---|
| Nome do projeto | Bloqueado para edição. |
| Objetivo | Bloqueado para edição. |
| Seletor de workbook | Bloqueado para alteração. |
| Botão de submissão | Desabilitado e rotulado “Analisando estrutura…”. |
| Painel de processo | Anunciado de forma educada a leitores de tela, sem estimar percentual. |

As provas em `client/src/pages/Home.test.tsx` forçam `analyze.isPending=true` e verificam o painel, a ausência de percentual simulado e os atributos `disabled` dos três controles de edição. `client/src/components/AnalysisFlowState.test.tsx` cobre a composição semântica do painel isolado.
