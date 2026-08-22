# MDL-UNDEFINED-020 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris, do gate de reconstrução e de nova autorização específica para implementar.

## Perfil privado proposto

A futura regra deverá receber somente um perfil agregado por aba. Os campos permitidos são `observed_row_count`, `physical_column_count`, `grain_evaluation_completed`, `evaluated_table_classifier_count`, `positive_table_classifier_count`, `classification_conflict_present`, `classification_ambiguity_present`, `formula_present_in_used_signals` e `sensitivity_present`.

O profiling transitório poderá consultar os resultados agregados das cinco classificações de tabela autorizadas para determinar completude e contagens, mas deverá descartar imediatamente a identidade de cada regra antes da projeção canônica da MDL-UNDEFINED-020. Valores, cabeçalhos, posições, títulos de aba, dados temporais, identificadores, rótulos de categoria, exemplos, frequências individuais e qualquer dado sensível são proibidos no perfil persistível e na evidência emitida.

## Condição determinística proposta

1. Exigir `observed_row_count >= 20`.
2. Exigir `physical_column_count >= 2`.
3. Exigir `grain_evaluation_completed == true`.
4. Exigir `evaluated_table_classifier_count == 5`, representando somente o conjunto fechado de classificadores draft autorizados na política.
5. Exigir `positive_table_classifier_count == 0`.
6. Exigir `classification_conflict_present == false` e `classification_ambiguity_present == false`.
7. Exigir `formula_present_in_used_signals == false` e `sensitivity_present == false`.
8. Emitir `table_classification_undefined_candidate` somente quando todas as condições forem satisfeitas.

O classificador futuro não deverá converter “nenhuma hipótese positiva” em inferência semântica, classificação de negócio ou recomendação de modelagem. Seu único resultado permitido é uma hipótese residual para revisão humana.

## Saída canônica proposta

Quando as guardas forem satisfeitas, a regra deverá projetar no campo canônico de classificação por aba uma hipótese `table_classification_undefined_candidate`, com versão futura `MDL-UNDEFINED-020@0.1.0-provisional.1`, severidade `review_required`, confiança `0.60`, evidência agregada e pergunta humana bloqueante. A saída não poderá incluir a identidade das classificações avaliadas, nem informação de origem da planilha.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| 20+ linhas, duas colunas, avaliação completa, zero hipóteses positivas e zero bloqueios | candidato residual com pergunta bloqueante |
| 19 linhas | sem candidato |
| Apenas uma coluna física | sem candidato |
| Avaliação de granularidade incompleta | sem candidato |
| Menos de cinco classificadores avaliados | sem candidato |
| Uma ou mais hipóteses positivas | sem candidato |
| Conflito ou ambiguidade presente | sem candidato |
| Fórmula nos sinais usados ou sensibilidade presente | sem candidato |
| Evidência que tente reter cabeçalho, valor, posição ou título de aba | falha de privacidade |

## Bloqueio

Não há implementação autorizada. A Proposta A não modifica o catálogo, o registro de classificadores, o contrato, o pipeline, a interface, os datasets golden ou o Gate MVP; também não habilita execução draft nem produção.
