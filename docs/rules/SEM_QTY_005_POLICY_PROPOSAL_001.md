# SEM-QTY-005 — Proposta de Política 001

**Regra:** `SEM-QTY-005` — Quantidade.  
**Estado:** proposta não executável; execução bloqueada.  
**Escopo oficial recuperado:** regra P0 por coluna, na etapa `semantic_typing`, dependente de qualidade e com saída `semantic_type`.

## Lacuna oficial e princípio conservador

O blueprint oficial determina que a regra deve classificar uma coluna como quantidade mediante evidências convergentes, porém não define condição, exclusões, confiança, evidências, perguntas ou calibração. A Proposta A reduz inferências de negócio: ela não converte números em quantidade pela aparência, não aceita números armazenados como texto e não usa o nome integral de uma coluna como evidência persistida.

## Proposta A — quantidade candidata

Uma coluna será classificada como `quantity_candidate` somente quando todos os critérios forem verdadeiros: o nome normalizado pertencer ao vocabulário fechado `quantidade`, `qtd` ou `qtde`; a coluna tiver ao menos 10 valores numéricos físicos finitos; o tipo físico for numérico; não houver fórmulas; não houver candidatos numéricos textuais nem valores numéricos ambíguos; e a regra de data genérica não tiver classificado a coluna como data.

O sinal de cabeçalho será processado transitoriamente e transformado apenas no booleano agregado `header_eligible`; cabeçalho, valores, posições, nomes de aba, identificadores e hashes serão descartados. A hipótese receberá confiança inicial de **0,75** e incluirá confirmação humana bloqueante: **“Esta coluna representa uma quantidade física ou contagem de unidades, e não preço, saldo, código, percentual ou outra medida?”**

| Elemento | Política proposta |
|---|---|
| Base mínima | 10 números físicos finitos |
| Tipo físico | `numeric` |
| Vocabulário fechado | `quantidade`, `qtd`, `qtde` |
| Integridade | Sem fórmulas, candidatos numéricos textuais ou ambiguidades numéricas |
| Exclusão temporal | Sem classificação semântica de data |
| Classificação | `quantity_candidate` |
| Confiança | `0.75` |
| Pergunta | Obrigatória e bloqueante |
| Saída | Fragmento canônico `semantic_type` com evidências agregadas |

## Exclusões e privacidade

Ficam excluídas colunas com menos de 10 números físicos, tipo texto, tipo misto, booleano, data, fórmulas, valores não finitos, números textuais ou ambíguos, cabeçalho fora do vocabulário fechado, ou classificação de data. A regra não deverá usar `idade`, `volume`, `estoque`, moeda, preço, valor, saldo, percentual ou qualquer sinônimo aberto como evidência de quantidade. Assim, ela não reaproveita indevidamente a elegibilidade específica da QLT-NEGATIVE-011, cujo vocabulário atende a uma finalidade distinta.

## Alternativa B — medida numérica genérica

Uma alternativa seria classificar toda coluna numérica sem fórmula como quantidade. Ela aumenta cobertura, mas conflita com identificadores, datas seriais, valores financeiros, percentuais e medidas de saldo. A Proposta A privilegia precisão e deixa os demais tipos para regras semânticas próprias e autorizadas.

## Condição de avanço

Esta proposta não autoriza implementação. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, perfil privado, classificador determinístico, registro semântico, integração canônica, testes positivos/negativos/limítrofes, golden dataset assinado, calibração reprodutível, gate individual e ativação exclusivamente no perfil draft. Produção permanece bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 20, `SEM-QTY-005`.
2. `artifacts/catalogs/rule-implementation-readiness-v1.json`, registro `SEM-QTY-005`.
3. `engine/profiling/numeric_text.py` e `engine/profiling/negative_values.py`, perfis privados reutilizáveis como restrições de integridade, não como semântica de negócio.
