# MDL-FACTTXN-002 — Proposta de Política 001

## Proposta A — hipótese conservadora de fato transacional

A aba será classificada como candidata a `fact_transactional` somente quando existir granularidade válida, no mínimo 20 linhas não vazias, uma chave temporal reconhecida com alta variabilidade de valores e ao menos uma medida numérica física elegível. A regra não presume uma transação por linha como verdade; ela emite uma hipótese com confiança 0,70 e uma pergunta humana obrigatória.

As evidências são exclusivamente agregadas: base avaliada, contagem de candidatos temporais, diversidade temporal e contagem de medidas elegíveis. A regra não emite valores, cabeçalhos, posições, títulos de aba nem períodos. Serão excluídas abas sem granularidade, bases inferiores a 20 linhas, tabelas de fato periódica confirmadas, fórmulas e colunas sem medida física.

## Estado

Esta proposta não é implementação, não autoriza execução e depende de aprovação explícita de Chris.
