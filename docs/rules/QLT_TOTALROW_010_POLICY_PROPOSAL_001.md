# QLT-TOTALROW-010 — Política proposta 001

**Estado:** proposta não executável, pendente de aprovação explícita de Chris.  
**Regra:** `QLT-TOTALROW-010 — Linhas totalizadoras`.  
**Fonte de metadados:** `PM-MVP-PBI-RULE-BP-001`, sequência 10.  
**Escopo oficial:** aba; prioridade P0; dependência `profiling`; saída `finding`.

## Objetivo e limitação

A fonte oficial determina a detecção de totais e subtotais dentro da tabela, mas não materializa vocabulário, critério de posição, verificação aritmética ou ações corretivas. Esta proposta reconstrói apenas um subconjunto técnico e observável, sem inferir a intenção de negócio nem expor conteúdos da planilha.

## Opção A proposta — rótulo português estrito com sinal numérico

Uma linha não vazia será candidata somente quando cumprir todos os critérios abaixo durante a leitura efêmera da aba:

| Critério | Regra conservadora proposta |
|---|---|
| Contexto anterior | A linha ocorre após pelo menos três linhas anteriores com conteúdo. |
| Célula de rótulo | A primeira célula com conteúdo é texto. |
| Normalização técnica | Aplicar apenas NFKC, conversão de quebras de linha em espaço, trim, redução de espaços internos e `casefold`. |
| Vocabulário fechado | O texto normalizado é exatamente `total`, `subtotal` ou `total geral`. |
| Sinal complementar | Existe pelo menos um número físico (`int` ou `float`, excluído booleano e `NaN`) em outra célula da mesma linha. |
| Gatilho | Emitir finding quando houver ao menos uma linha candidata. |

O perfil preservará exclusivamente contagem de linhas não vazias, contagem de linhas candidatas, proporção e base de normalização. A implementação não reterá rótulos, números, fórmulas, posições físicas, títulos de abas, nomes de colunas ou valores de célula.

## Severidade e pergunta humana

| Proporção de candidatas entre linhas não vazias | Severidade | Pergunta de validação |
|---|---|---|
| Até 5% | Baixa | Não emitir pergunta. |
| Acima de 5% até 20% | Média | Perguntar se as linhas agregadas devem ser excluídas antes da modelagem. |
| Acima de 20% | Alta | Perguntar se as linhas agregadas representam estrutura de relatório e exigem separação prévia. |

## Exclusões mandatórias

Ficam excluídas linhas antes da terceira observação não vazia, rótulos fora do vocabulário fechado, valores `Decimal`, números serializados em texto, fórmulas, datas, booleanos, checagem de igualdade entre total e parcelas, vocabulários em outros idiomas, subtotais sem sinal numérico e qualquer interpretação de semântica de negócio. A regra não remove, transforma, marca nem reordena linhas.

> Esta proposta não autoriza código, execução, allowlist ou produção. A implementação só poderá ocorrer após gate de reconstrução com aprovação explícita de Chris.
