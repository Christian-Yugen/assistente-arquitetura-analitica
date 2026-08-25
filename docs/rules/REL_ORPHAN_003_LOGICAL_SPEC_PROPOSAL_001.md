# REL-ORPHAN-003 — Especificação Lógica Proposta 001

## Limites e entrada permitida

A futura regra receberá somente um perfil privado por par de abas, composto por contagens e booleanos agregados. As entradas propostas incluem classificações agregadas das tabelas, quantidade de linhas observadas, quantidade de chaves e referências elegíveis, completude, unicidade da chave e da referência, cobertura referencial, contagem agregada de referências não cobertas, presença de fórmulas, presença de sensibilidade, quantidade de direções elegíveis, autorreferência, conflito e ambiguidade.

Qualquer comparação transitória necessária para calcular cobertura ou referências não cobertas existirá somente em memória durante a requisição e será descartada antes da construção do perfil. Cabeçalhos, valores, nomes e títulos de abas, posições, identificadores, pares correspondentes, exemplos e frequências individuais são proibidos no perfil persistível, nas evidências, no contrato e nos logs.

## Guardas determinísticas propostas

A emissão futura exigirá simultaneamente: `source_standard_dimension_candidate = true`; `target_fact_candidate = true` para fato transacional ou periódico; abas distintas; `eligible_dimension_key_count = 1`; `eligible_fact_reference_count = 1`; `dimension_key_complete = true`; `dimension_key_unique = true`; `fact_reference_complete = true`; `fact_reference_unique = false`; `referential_coverage_ratio > 0.0`; `referential_coverage_ratio < 1.0`; `uncovered_reference_distinct_count > 0`; e `eligible_direction_count = 1`.

A emissão será bloqueada por fórmula, sinal sensível, chave ou referência incompleta, cobertura igual a `0.0` ou `1.0`, ausência de correspondências, relação 1:1, padrão muitos-para-muitos, autorreferência, dimensão calendário, fato sem granularidade definida, classificação indefinida, conflito de classificação, mais de uma chave ou referência elegível, mais de uma direção elegível ou qualquer ambiguidade. A futura regra não deve emitir hipótese para identificar valores órfãos ou recomendar uma correção.

## Saída proposta

Quando todas as guardas forem satisfeitas, a futura regra emitirá `orphan_reference_candidate`, confiança `0.80`, severidade `warning`, evidências somente agregadas e uma pergunta humana bloqueante para revisar a cobertura referencial parcial. A saída não confirma chave primária, chave estrangeira, integridade referencial, erro de negócio, direção de filtro, cardinalidade final ou relacionamento no Power BI.

## Precedência e coexistência

A regra depende de classificações de tabela já emitidas e não as substitui. Ela não executará sobre tabelas com classificação indefinida, fato sem granularidade, dimensão calendário ou estado conflitante. Ela deverá coexistir com a REL-ONEMANY-001 como diagnóstico de bloqueio: cobertura parcial impede uma hipótese 1:N no mesmo candidato, mas não transforma esta regra em recomendação de relacionamento.

## Estado de autorização

Esta especificação é não executável e permanece bloqueada até aprovação específica de Chris para a Proposta A e gate de reconstrução formalizado. Uma aprovação de política não autoriza a escrita, integração ou execução de código.
