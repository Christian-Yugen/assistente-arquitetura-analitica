# MDL-DIMSTD-004 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris.

## Entrada mínima privada

O perfil por aba deverá conter apenas `observed_row_count`, `grain_available`, contagem de identificadores semanticamente elegíveis, contagem de identificadores individuais completos e únicos, contagem de atributos textuais descritivos elegíveis, contagem de medidas numéricas elegíveis e contagem de colunas temporais integralmente reconhecidas. Nenhum valor, cabeçalho, posição, nome de aba ou identificador poderá ser retido.

## Condição determinística proposta

1. Exigir `grain_available == true`.
2. Exigir `observed_row_count >= 20`.
3. Exigir ao menos um identificador elegível com cobertura e unicidade individuais de `1.0`.
4. Exigir ao menos um atributo textual descritivo elegível com razão de distintos entre `0.05` e `0.90`.
5. Exigir `eligible_measure_column_count == 0`.
6. Exigir `fully_recognized_temporal_column_count == 0`.
7. Emitir `dimension_standard_candidate` somente quando todas as condições forem satisfeitas.

## Saída canônica proposta

O candidato deverá ser projetado no campo canônico de classificação por aba, com versão de regra, confiança `0.70`, evidência agregada e pergunta humana bloqueante. A pergunta deve apontar que a resposta confirma ou rejeita a hipótese, sem exibir dados de origem. Ausência de candidato não será convertida em classificação negativa ou indefinida explícita.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| Chave única, atributo descritivo e ausência de medidas/datas | candidato de dimensão cadastral |
| Base com 19 linhas | sem candidato |
| Sem granularidade | sem candidato |
| Sem identificador individualmente único | sem candidato |
| Sem atributo descritivo | sem candidato |
| Com medida elegível | sem candidato |
| Com data integralmente reconhecida | sem candidato |

## Bloqueio

Não há perfil, classificador, registro, versão de contrato, integração de pipeline, testes executáveis, dataset golden, calibração ou allowlist autorizados enquanto o gate de reconstrução não for aprovado por Chris.
