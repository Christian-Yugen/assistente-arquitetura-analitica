# SEM-ACTUAL-014 — Proposta de Política 001

**Regra:** `SEM-ACTUAL-014` — Realizado.  
**Estado:** proposta não executável; execução bloqueada.  
**Escopo oficial recuperado:** regra P0 por coluna, na etapa `semantic_typing`, dependente de qualidade e com saída `semantic_type`.

## Lacuna oficial e princípio conservador

O blueprint oficial determina a classificação de uma coluna como realizado por evidências convergentes, mas não define condição, vocabulário, exclusões, confiança, evidência, pergunta, testes ou calibração. A Proposta A limita a inferência a cabeçalhos fechados e inequívocos combinados com uma base numérica física íntegra. Ela não deduz realização por magnitude, distribuição, períodos, fórmulas, nomes de abas, conteúdo de outras colunas ou conhecimento externo.

## Proposta A — realizado candidato

Uma coluna será classificada como `actual_candidate` somente quando todos os critérios forem verdadeiros: o cabeçalho normalizado pertencer ao vocabulário fechado `realizado`, `valor realizado`, `realizado total`, `executado`, `valor executado`, `observado` ou `actual`; o tipo físico da coluna for numérico; houver ao menos 10 números físicos finitos; não houver fórmulas, candidatos numéricos textuais ou ambiguidades numéricas; e a coluna não for integralmente reconhecida como data.

O perfil reduzirá o cabeçalho a um booleano de elegibilidade e os valores a contagens agregadas já disponíveis. Não reterá cabeçalho, valores, fórmulas, posições, títulos de abas, períodos, identificadores ou hashes. A hipótese terá confiança inicial de **0,75** e incluirá a pergunta humana bloqueante: **“Esta coluna representa o valor efetivamente realizado ou observado que deve ser distinguido de metas, previsões e parâmetros na modelagem?”**

| Elemento | Política proposta |
|---|---|
| Base mínima | 10 números físicos finitos |
| Tipo físico | `numeric` |
| Vocabulário fechado | `realizado`, `valor realizado`, `realizado total`, `executado`, `valor executado`, `observado`, `actual` |
| Integridade | Sem fórmulas, candidatos numéricos textuais ou ambiguidades numéricas |
| Exclusão temporal | Sem classificação semântica de data |
| Classificação | `actual_candidate` |
| Confiança | `0.75` |
| Pergunta | Obrigatória e bloqueante |
| Saída | Fragmento canônico `semantic_type` com evidências agregadas |

## Exclusões e privacidade

Ficam excluídas colunas com menos de 10 números físicos finitos; tipos texto, misto, booleano ou data; fórmulas; números textuais ou ambíguos; cabeçalho fora do vocabulário fechado; ou classificação de data. A regra não infere unidade, moeda, percentual, horizonte temporal, período contábil, centro de custo, responsável, tipo de planejamento ou qualidade do resultado. Os termos isolados `real`, `atual` e `resultado` permanecem deliberadamente fora do vocabulário por serem ambíguos em contexto de planilha.

## Alternativa B — inferência por distribuição ou vocabulário amplo

Uma alternativa seria admitir expressões compostas, nome de aba, período, fórmulas ou padrões numéricos como evidência. Ela elevaria a cobertura aparente, mas criaria confusão entre valores realizados, projeções, limites, parâmetros, status e medidas operacionais. A Proposta A privilegia precisão, rastreabilidade e confirmação humana; qualquer ampliação exige novo intake, política, calibração e autorização explícita.

## Condição de avanço

Esta proposta não autoriza implementação. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, perfil privado, classificador determinístico, registro semântico, versão de contrato, integração canônica, testes positivos/negativos/limítrofes, golden dataset assinado, calibração reprodutível, gate individual e ativação exclusivamente em draft. Produção permanece bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 29, `SEM-ACTUAL-014`.
2. `artifacts/catalogs/rule-implementation-readiness-v1.json`, registro `SEM-ACTUAL-014`.
3. `artifacts/intake/SEM-ACTUAL-014.json`, lacunas e pré-condições recuperadas.
