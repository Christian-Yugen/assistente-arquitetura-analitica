# Escopo de Recomendações de Power Query e DAX 001

## Decisão de produto registrada

Chris confirmou que o objetivo final do Assistente de Arquitetura Analítica é preparar uma planilha para a construção responsável de um dashboard: diagnosticar qualidade e estrutura, sugerir modelagem dimensional, apontar relacionamentos, recomendar transformações de dados e propor medidas. Esta decisão amplia a orientação do produto, mas **não autoriza geração automática, execução de código M, execução de DAX, alteração de arquivos, alteração de modelos Power BI ou produção**.

## DAX revisável

A regra oficial `MET-DAX-015 — DAX derivado da fórmula conceitual` reserva o slot de catálogo para sugestão ou validação de DAX a partir de uma métrica conceitual. Sua futura implementação somente poderá emitir uma sugestão quando uma métrica anterior estiver explicitamente definida por sinais agregados, tipagem semântica e granularidade compatíveis, sem conflito ou ambiguidade material.

Uma sugestão DAX deverá conter fórmula conceitual, expressão proposta, dependências opacas, limitações, confiança limitada e pergunta humana bloqueante. Ela não poderá inferir regra de negócio ausente, criar medidas no Power BI ou apresentar o código como fórmula final aprovada.

## Power Query revisável

O catálogo de 95 regras ainda não contém um gerador completo de M/Power Query. As regras de qualidade e estrutura podem identificar a necessidade de transformações, mas não autorizam por si só produzir ou executar código de consulta.

O produto poderá evoluir para recomendações como uma camada de **plano de transformação**, não como automação cega. Cada recomendação futura deverá indicar somente a operação conceitual, justificativa agregada, risco, pré-condições e confirmação humana necessária.

| Tipo | Intenção permitida | Limite obrigatório |
|---|---|---|
| Limpeza | Padronizar espaços e revisar vazios ou tipos mistos | Nunca apagar ou substituir valores automaticamente. |
| Tipagem | Converter candidatos numéricos, datas ou percentuais | Exigir elegibilidade agregada e bloquear ambiguidade. |
| Estrutura | Sugerir cabeçalho ou revisão de tabela desnormalizada | Não inferir contexto de negócio a partir de conteúdo livre. |
| Qualidade | Isolar duplicidades, totalizadores ou órfãos para revisão | Não deduplicar, excluir ou consolidar registros automaticamente. |

Caso o produto passe a gerar M, o código deverá ser um **rascunho exportável**, associado ao diagnóstico e à aprovação humana, sem conexão automática à origem de dados ou execução dentro do produto.

## Dependências de governança

Antes de qualquer recomendação DAX ou Power Query tornar-se executável em draft, aplicam-se intake, política conservadora, aprovação de Chris, gate de reconstrução, autorização específica de implementação, perfil privado, testes positivos e negativos, dataset sintético, manifesto verificável, calibração TP/FP/FN, gate individual e allowlist draft.

Produção continua bloqueada até a conclusão do conjunto de regras, controles de privacidade, calibração operacional, retenção física verificável e experiência de revisão humana.
