# SEM-PCT-007 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris.

## Perfil privado proposto

O perfil por coluna deverá conter somente `physical_type`, `formula_count`, `header_eligible`, `physical_numeric_count`, `in_range_numeric_count`, `numeric_text_candidate_count`, `numeric_text_ambiguity_count` e o sinal agregado da classificação de data. A normalização de cabeçalho usará NFKC, casefold, remoção de acentos e colapso de espaços durante o profiling; o texto normalizado não será persistido. Valores, posições, título de aba, hash e identificadores serão descartados.

## Condição determinística proposta

1. Exigir `header_eligible == true` para o vocabulário fechado `percentual`, `percentagem`, `pct`, `%`.
2. Exigir `physical_type == "numeric"`.
3. Exigir `physical_numeric_count >= 10`.
4. Exigir `in_range_numeric_count == physical_numeric_count`, para o intervalo fechado `[0, 1]`.
5. Exigir `formula_count == 0`.
6. Exigir `numeric_text_candidate_count == 0` e `numeric_text_ambiguity_count == 0`.
7. Exigir ausência de candidato `date_generic` emitido pela SEM-DATE-001 para a mesma coluna.
8. Emitir `percentage_candidate` somente quando todas as condições forem satisfeitas.

## Saída canônica proposta

O candidato deverá ser adicionado à coleção canônica `semantic_classifications`, com `rule_id`, versão de regra, `semantic_type` igual a `percentage_candidate`, confiança `0.75`, evidência agregada e pergunta humana bloqueante. A ausência de candidato não deverá gerar tipagem negativa ou revelar o cabeçalho de origem.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| `Percentual` com 10 ou mais números físicos entre zero e um | candidato de percentual |
| `pct` ou `%` com números físicos entre zero e um | candidato de percentual |
| Cabeçalho fora do vocabulário | sem candidato |
| Base de 9 números físicos | sem candidato |
| Valor físico maior que um ou negativo | sem candidato |
| Número armazenado como texto ou ambíguo | sem candidato |
| Fórmula presente | sem candidato |
| Data genericamente reconhecida | sem candidato |

## Bloqueio

Não há perfil, classificador, registro, versão de contrato, integração de pipeline, testes executáveis, dataset golden, calibração ou allowlist autorizados enquanto o gate de reconstrução não for aprovado por Chris.
