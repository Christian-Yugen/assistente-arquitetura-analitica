# REL-NONUNIQ-002 — Especificação Lógica Proposta 001

## Limites e entrada permitida

A futura regra receberá somente um perfil privado por par de abas, composto por contagens e booleanos agregados. As entradas propostas incluem classificações agregadas das tabelas, quantidade de linhas observadas, quantidade de chaves e referências elegíveis, completude, unicidade agregada da chave dimensional, contagem agregada de duplicidades no lado dimensional, cobertura referencial, presença de fórmulas, presença de sensibilidade, quantidade de direções elegíveis, autorreferência, conflito e ambiguidade.

Qualquer comparação transitória necessária para cobertura referencial ou contagem de duplicidade existirá somente em memória durante a requisição e será descartada antes da construção do perfil. Cabeçalhos, valores, nomes e títulos de abas, posições, identificadores, pares correspondentes, exemplos e frequências individuais são proibidos no perfil persistível, nas evidências, no contrato e nos logs.

## Guardas determinísticas propostas

A emissão futura exigirá simultaneamente: `source_standard_dimension_candidate = true`; `target_fact_candidate = true` para fato transacional ou periódico; abas distintas; `eligible_dimension_key_count = 1`; `eligible_fact_reference_count = 1`; `dimension_key_complete = true`; `dimension_key_unique = false`; `dimension_key_duplicate_count > 0`; `fact_reference_complete = true`; `referential_coverage_ratio = 1.0`; e `eligible_direction_count = 1`.

A emissão será bloqueada por fórmula, sinal sensível, chave ou referência incompleta, cobertura inferior a `1.0`, ausência de correspondências, relação 1:1, padrão muitos-para-muitos, autorreferência, dimensão calendário, fato sem granularidade definida, classificação indefinida, conflito de classificação, mais de uma chave ou referência elegível, mais de uma direção elegível ou qualquer ambiguidade. A futura regra não deve emitir hipótese para inferir qual valor está duplicado ou qual correção operacional é adequada.

## Saída proposta

Quando todas as guardas forem satisfeitas, a futura regra emitirá `one_side_key_non_unique_candidate`, confiança `0.80`, severidade `warning`, evidências somente agregadas e uma pergunta humana bloqueante para revisar a unicidade do lado 1. A saída não confirma chave primária, chave estrangeira, duplicidade de negócio, direção de filtro, cardinalidade final ou relacionamento no Power BI.

## Precedência e coexistência

A regra depende de classificações de tabela já emitidas e não as substitui. Ela não executará sobre tabelas com classificação indefinida, fato sem granularidade, dimensão calendário ou estado conflitante. Ela deverá coexistir com a REL-ONEMANY-001 como diagnóstico de bloqueio: a presença de não unicidade impede uma hipótese 1:N no mesmo candidato, mas não transforma esta regra em recomendação de relacionamento.

## Estado de autorização

Esta especificação é não executável e permanece bloqueada até aprovação específica de Chris para a Proposta A e gate de reconstrução formalizado. Uma aprovação de política não autoriza a escrita, integração ou execução de código.
