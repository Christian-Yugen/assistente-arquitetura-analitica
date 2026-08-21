# SEM-TARGET-013 — Proposta de Política 001

**Regra:** `SEM-TARGET-013` — Meta ou previsto.  
**Estado:** proposta não executável; execução bloqueada.  
**Escopo oficial recuperado:** regra P0 por coluna, na etapa `semantic_typing`, dependente de qualidade e com saída `semantic_type`.

## Lacuna oficial e princípio conservador

O blueprint oficial determina a classificação de uma coluna como meta ou previsto por evidências convergentes, mas não define condição, vocabulário, exclusões, confiança, evidência, pergunta, testes ou calibração. A Proposta A limita a inferência a cabeçalhos fechados e inequívocos combinados com uma base numérica física íntegra. Ela não deduz intenção de planejamento por magnitude, distribuição, períodos, fórmulas, nomes de abas, conteúdo de outras colunas ou conhecimento externo.

## Proposta A — meta ou previsto candidato

Uma coluna será classificada como `target_or_forecast_candidate` somente quando todos os critérios forem verdadeiros: o cabeçalho normalizado pertencer ao vocabulário fechado `meta`, `previsto`, `previsao`, `orcado`, `orcamento`, `forecast`, `target`, `budget` ou `planejado`; o tipo físico da coluna for numérico; houver ao menos 10 números físicos finitos; não houver fórmulas, candidatos numéricos textuais ou ambiguidades numéricas; e a coluna não for integralmente reconhecida como data.

O perfil reduzirá o cabeçalho a um booleano de elegibilidade e os valores a contagens agregadas já disponíveis. Não reterá cabeçalho, valores, fórmulas, posições, títulos de abas, períodos, identificadores ou hashes. A hipótese terá confiança inicial de **0,75** e incluirá a pergunta humana bloqueante: **“Esta coluna representa uma meta, plano ou previsão que deve ser distinguida do valor realizado na modelagem?”**

| Elemento | Política proposta |
|---|---|
| Base mínima | 10 números físicos finitos |
| Tipo físico | `numeric` |
| Vocabulário fechado | `meta`, `previsto`, `previsao`, `orcado`, `orcamento`, `forecast`, `target`, `budget`, `planejado` |
| Integridade | Sem fórmulas, candidatos numéricos textuais ou ambiguidades numéricas |
| Exclusão temporal | Sem classificação semântica de data |
| Classificação | `target_or_forecast_candidate` |
| Confiança | `0.75` |
| Pergunta | Obrigatória e bloqueante |
| Saída | Fragmento canônico `semantic_type` com evidências agregadas |

## Exclusões e privacidade

Ficam excluídas colunas com menos de 10 números físicos finitos; tipos texto, misto, booleano ou data; fórmulas; números textuais ou ambíguos; cabeçalho fora do vocabulário fechado; ou classificação de data. A regra não infere unidade, moeda, percentual, horizonte temporal, versão de orçamento, centro de custo, responsável ou valor realizado. Cabeçalhos compostos, abreviações não listadas e contexto de negócio exigem nova proposta formal.

## Alternativa B — inferência por distribuição ou vocabulário amplo

Uma alternativa seria admitir expressões compostas, nome de aba, período, fórmulas ou padrões numéricos como evidência. Ela elevaria a cobertura aparente, mas criaria confusão entre valores realizados, projeções, limites, parâmetros e medidas operacionais. A Proposta A privilegia precisão, rastreabilidade e confirmação humana; qualquer ampliação exige novo intake, política, calibração e autorização explícita.

## Condição de avanço

Esta proposta não autoriza implementação. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, perfil privado, classificador determinístico, registro semântico, versão de contrato, integração canônica, testes positivos/negativos/limítrofes, golden dataset assinado, calibração reprodutível, gate individual e ativação exclusivamente em draft. Produção permanece bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 28, `SEM-TARGET-013`.
2. `artifacts/catalogs/rule-implementation-readiness-v1.json`, registro `SEM-TARGET-013`.
3. `artifacts/intake/SEM-TARGET-013.json`, lacunas e pré-condições recuperadas.
