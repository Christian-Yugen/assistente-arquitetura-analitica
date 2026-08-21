# SEM-PCT-007 — Proposta de Política 001

**Regra:** `SEM-PCT-007` — Percentual.  
**Estado:** proposta não executável; execução bloqueada.  
**Escopo oficial recuperado:** regra P0 por coluna, na etapa `semantic_typing`, dependente de qualidade e com saída `semantic_type`.

## Lacuna oficial e princípio conservador

O blueprint oficial determina a classificação de uma coluna como percentual com evidências convergentes, mas não define condição, exclusões, confiança, evidência, pergunta ou calibração. A Proposta A limita a inferência a uma representação proporcional inequívoca: números físicos finitos no intervalo fechado de zero a um. Ela não interpreta percentuais baseados em escala de zero a cem, formatação visual do Excel, textos com símbolo de porcentagem, expressões, moeda, indicadores, índices ou sinônimos abertos.

## Proposta A — percentual candidato

Uma coluna será classificada como `percentage_candidate` somente quando todos os critérios forem verdadeiros: seu cabeçalho normalizado pertencer ao vocabulário fechado `percentual`, `percentagem`, `pct` ou `%`; ela tiver ao menos 10 números físicos finitos; todos os números físicos estiverem no intervalo fechado `[0, 1]`; não houver fórmulas, candidatos numéricos textuais, ambiguidades numéricas nem classificação semântica de data.

O nome de cabeçalho será processado transitoriamente e reduzido ao booleano agregado `header_eligible`; os valores serão avaliados apenas para obter contagens agregadas de números físicos e de observações dentro do intervalo. Cabeçalhos, valores, posições, nomes de aba, identificadores e hashes não poderão compor o perfil persistido ou a saída canônica. A hipótese terá confiança inicial de **0,75** e incluirá a pergunta humana bloqueante: **“Esta coluna representa uma proporção ou taxa expressa de zero a um, e não uma medida, índice, código ou valor decimal de outra natureza?”**

| Elemento | Política proposta |
|---|---|
| Base mínima | 10 números físicos finitos |
| Tipo físico | `numeric` |
| Vocabulário fechado | `percentual`, `percentagem`, `pct`, `%` |
| Codificação aceita | Todos os valores físicos no intervalo `[0, 1]` |
| Integridade | Sem fórmulas, candidatos numéricos textuais ou ambiguidades numéricas |
| Exclusão temporal | Sem classificação semântica de data |
| Classificação | `percentage_candidate` |
| Confiança | `0.75` |
| Pergunta | Obrigatória e bloqueante |
| Saída | Fragmento canônico `semantic_type` com evidências agregadas |

## Exclusões e privacidade

Ficam excluídas colunas com menos de 10 números físicos, tipo texto, misto, booleano ou data; fórmulas; números textuais ou ambíguos; cabeçalho fora do vocabulário fechado; valores físicos negativos, superiores a um ou não finitos; ou classificação de data. O símbolo `%` será aceito somente se corresponder ao cabeçalho completo após normalização, e não como parte de uma busca livre.

## Alternativa B — suporte a escala zero a cem

Uma alternativa seria aceitar colunas inteiramente no intervalo `[0, 100]`. Ela cobriria uma prática comum, mas também confundiria percentuais com contagens, notas, códigos e medidas. A Proposta A privilegia precisão e deixa a escala de zero a cem para uma futura ampliação versionada, que exigirá novo intake, política, calibração e autorização explícita.

## Condição de avanço

Esta proposta não autoriza implementação. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, perfil privado, classificador determinístico, registro semântico, integração canônica, testes positivos/negativos/limítrofes, golden dataset assinado, calibração reprodutível, gate individual e ativação exclusivamente em draft. Produção permanece bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 22, `SEM-PCT-007`.
2. `artifacts/catalogs/rule-implementation-readiness-v1.json`, registro `SEM-PCT-007`.
3. `engine/profiling/semantic_quantity.py`, exemplo de perfil agregado de cabeçalho normalizado e números físicos.
