# MDL-DIMCAL-006 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris.

## Perfil privado proposto

O perfil por aba deverá conter somente `observed_row_count`, `grain_available`, quantidade de colunas de data integralmente reconhecidas, maior contagem de datas reconhecidas, maior contagem de datas distintas, maior contagem de transições consecutivas de um dia e quantidade de medidas numéricas físicas elegíveis. A ordenação e a comparação de datas ocorrem transitoriamente e são descartadas antes da saída. Nenhuma data, valor, cabeçalho, posição, nome de aba ou hash poderá ser retido.

## Condição determinística proposta

1. Exigir `grain_available == true`.
2. Exigir `observed_row_count >= 20`.
3. Exigir ao menos uma coluna física com razão de reconhecimento de data igual a `1.0`.
4. Exigir `distinct_date_count == recognized_date_count` nessa coluna.
5. Exigir `consecutive_day_transition_count == distinct_date_count - 1`.
6. Exigir `eligible_measure_column_count == 0`.
7. Emitir `dimension_calendar_candidate` somente quando todas as condições forem satisfeitas.

## Saída canônica proposta

O candidato deverá ser projetado no campo canônico de classificação por aba, com versão de regra, confiança `0.75`, evidência agregada e pergunta humana bloqueante. A falta de candidato não deverá gerar classificação negativa explícita nem expor evidência temporal de origem.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| Vinte ou mais dias consecutivos, únicos, sem medida | candidato de dimensão calendário |
| Base com 19 linhas | sem candidato |
| Sem granularidade | sem candidato |
| Datas repetidas | sem candidato |
| Lacuna de um ou mais dias | sem candidato |
| Coluna parcialmente reconhecida como data | sem candidato |
| Medida numérica física elegível | sem candidato |

## Bloqueio

Não há implementação autorizada enquanto o gate de reconstrução não for aprovado por Chris. A Proposta A também não amplia a semântica de datas, não suporta calendário mensal ou fiscal descontínuo e não substitui a confirmação humana.
