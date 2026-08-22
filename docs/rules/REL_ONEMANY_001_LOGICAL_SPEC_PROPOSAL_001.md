# REL-ONEMANY-001 — Especificação Lógica Proposta 001

## Limites e entrada permitida

A futura regra receberá somente um perfil privado por par de abas, composto por contagens e booleanos agregados. As entradas permitidas incluem classificação agregada da tabela, quantidade de linhas, quantidade de candidatos de chave e referência, completude agregada, unicidade agregada da chave, cardinalidade agregada da referência, cobertura referencial agregada, presença de fórmulas, presença de sensibilidade, quantidade de direções elegíveis, autorreferência e ambiguidade.

Qualquer comparação de valores para cobertura referencial será transitória, em memória e descartada antes da construção do perfil. Cabeçalhos, valores, nomes e títulos de abas, posições, identificadores, pares de correspondência, exemplos e frequências individuais são proibidos no perfil persistível, nas evidências, no contrato e nos logs.

## Guardas determinísticas propostas

A emissão futura exigirá simultaneamente: `source_standard_dimension_candidate = true`; `target_fact_candidate = true` para fato transacional ou periódico; abas distintas; `eligible_dimension_key_count = 1`; `eligible_fact_reference_count = 1`; `dimension_key_complete = true`; `dimension_key_unique = true`; `fact_reference_complete = true`; `fact_reference_unique = false`; `referential_coverage_ratio = 1.0`; e `eligible_direction_count = 1`.

A emissão será bloqueada por qualquer fórmula, sinal sensível, referência incompleta, cobertura inferior a 1,0, ausência de correspondências, relação 1:1, padrão muitos-para-muitos, autorreferência, dimensão calendário, fato sem granularidade definida, classificação indefinida, conflito de classificação, mais de uma chave ou referência elegível, mais de uma direção elegível ou qualquer ambiguidade.

## Saída proposta

Quando todas as guardas forem satisfeitas, a regra emitirá `one_to_many_relationship_candidate`, confiança `0.85`, severidade `info`, evidências somente agregadas e uma pergunta humana bloqueante para confirmar o relacionamento antes de criar qualquer relação no modelo. A saída não confirma chave primária, chave estrangeira, direção de filtro, cardinalidade final ou relacionamento no Power BI.

## Precedência e coexistência

A regra depende de classificações de tabela já emitidas e não as substitui. Ela não executará sobre tabelas com classificação indefinida, fato sem granularidade, dimensão calendário ou estado conflitante. A regra será suprimida quando houver mais de uma hipótese de relacionamento no mesmo par ou quando o par puder representar outra cardinalidade.

## Estado de autorização

Este documento é não executável e permanece bloqueado até aprovação específica de Chris para a Proposta A e gate de reconstrução formalizado. Uma aprovação de política não autoriza a escrita, integração ou execução de código.
