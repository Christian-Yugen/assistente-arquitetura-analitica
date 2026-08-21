# QLT-EMPTYROW-004 — Política Reconstruída de Linhas Vazias

**Versão candidata:** `0.1.0-reconstructed.1`.  
**Estado:** autorizada por Chris para especificação e implementação no perfil draft; não executável até o gate de calibração próprio.

## Origem, objetivo e limite de decisão

O blueprint oficial preserva o identificador `QLT-EMPTYROW-004`, o título **Linhas vazias**, prioridade `P1`, escopo de aba e o objetivo de detectar linhas totalmente vazias na região tabular. A fonte materializada de política não está disponível nesta cópia do repositório. Esta reconstrução registra a **opção A**, aprovada por Chris, e não reivindica recuperar o artefato original.

| Aspecto | Decisão reconstruída |
|---|---|
| Regra | `QLT-EMPTYROW-004` — Linhas vazias |
| Unidade de avaliação | Linha física de dados dentro de uma aba |
| População avaliada | Linhas após a linha de cabeçalho da região lida pelo workbook |
| Condição | Linha inteiramente vazia, localizada entre linhas com conteúdo observável |
| Saída | Um finding agregado por aba elegível |
| Ação automática | Proibida: não excluir, deslocar, preencher ou consolidar linhas |

## Definição de vazio e de posição elegível

Uma célula é vazia somente quando seu valor é nulo, ausente ou texto cujo conteúdo, após a remoção de espaços nas extremidades, é vazio. Valores `0`, `false`, datas, números, booleanos, fórmulas e texto não vazio **não** são vazios. Uma linha é inteiramente vazia quando todas as suas células observadas atendem essa definição.

Uma linha ou bloco contíguo de linhas inteiramente vazias é elegível somente se houver uma linha com conteúdo antes e outra depois do bloco, na mesma região de dados. Blocos iniciais e finais não são reportados. O perfil continua excluindo linhas inteiramente vazias dos demais cálculos para impedir que distorçam métricas de ausência, texto numérico, categorias e duplicidades.

> A regra evidencia uma possível quebra de continuidade tabular; ela não afirma erro de negócio e não autoriza alterar a planilha.

## Evidência, severidade e privacidade

O contexto, finding e persistência retêm apenas o identificador anonimizado da aba, a quantidade agregada de linhas vazias internas, a quantidade agregada de blocos e a quantidade de linhas com conteúdo avaliadas. Valores de células, números de linha, títulos brutos de aba, fórmulas e amostras são proibidos.

| Proporção de linhas vazias internas na região observada | Severidade | Pergunta de validação |
|---|---|---|
| Menor que 5% | Baixa | Não obrigatória |
| De 5% até menos de 20% | Média | Não obrigatória |
| 20% ou mais | Alta | Obrigatória |

A confiança-base é `0,95`. Ela é reduzida para `0,80` quando a aba tem somente duas linhas com conteúdo, porque a separação observada é mínima. Não há inferência de granularidade, chave de negócio ou significado de linha em branco.

## Exclusões, governança e promoção

A regra não considera lacunas no fim ou início da tabela, sentinelas, fórmulas sem resultado, células mescladas, linhas ocultas ou formatação visual. Ela não usa LLM e não produz modelagem dimensional. Extensões para interpretar sentinelas, seções, subtotais ou fórmulas exigem uma nova política e um novo gate.

A execução permanece bloqueada fora do perfil draft. A promoção exige implementação reproduzível, testes de privacidade, golden dataset, calibração, gate explícito e remoção dos bloqueios aplicáveis do Gate MVP 1.0.
