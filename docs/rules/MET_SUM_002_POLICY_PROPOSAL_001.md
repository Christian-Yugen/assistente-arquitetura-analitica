# MET-SUM-002 — Proposta A de Política 001

## Finalidade e limite

A `MET-SUM-002` é uma **recomendação conceitual revisável** de soma. Ela não calcula resultados, não escolhe campo, não identifica valores, não gera DAX/Power Query e não altera workbooks ou modelos Power BI.

> Um candidato semântico numérico não determina a unidade de medida, o filtro de negócio, a granularidade temporal nem se a agregação por soma é válida.

## Proposta A

A futura regra poderá emitir somente `sum_conceptual_metric_candidate` para uma aba opaca com 20+ linhas, duas ou mais colunas físicas, exatamente um candidato semântico de `quantity_candidate` ou `currency_candidate` e granularidade única definida. Sensibilidade, fórmulas, classificação indefinida, fato sem grão, conflito, ambiguidade de grão ou zero/múltiplos candidatos numéricos bloqueiam.

A saída terá no máximo confiança `0.60`, severidade `review_required`, fórmula conceitual `SUM(eligible_measure)` e pergunta bloqueante: **“Qual medida deve ser somada, em qual unidade e com quais filtros de negócio?”** Não há cálculo, DAX, M ou decisão automática.

## Privacidade e exclusões

O perfil futuro pode conter apenas contagens e flags agregadas. Valores, cabeçalhos, posições, frequências individuais, identificadores, unidades e fórmulas são proibidos. `SEM-SENS-015`, mascaramento e `sensitivity_classifications` bloqueiam de modo independente.

Esta proposta não autoriza classificador, perfil, contrato, pipeline, allowlist, teste executável, golden dataset, calibração, interface ou produção.
