# SEM-TARGET-013 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris.

## Perfil privado proposto

O perfil específico por coluna deverá conter somente `header_eligible`, `physical_numeric_count` e `basis`. A normalização do cabeçalho usará NFKC, `casefold`, remoção de acentos e colapso de espaços somente durante o profiling. O classificador combinará esse perfil com os sinais agregados já existentes de tipo físico, fórmulas, texto numérico e data sem persistir cabeçalho normalizado, valores, fórmulas, posições, títulos de abas, períodos, identificadores ou hashes.

## Condição determinística proposta

1. Exigir `header_eligible == true` para o vocabulário fechado definido na Proposta A.
2. Exigir `physical_type == "numeric"`.
3. Exigir `physical_numeric_count >= 10`.
4. Exigir `formula_count == 0`.
5. Exigir `numeric_text_candidate_count == 0` e `numeric_text_ambiguity_count == 0`.
6. Exigir ausência de candidato `date_generic` emitido pela SEM-DATE-001 para a mesma coluna.
7. Emitir `target_or_forecast_candidate` somente quando todas as condições forem satisfeitas.

## Saída canônica proposta

O candidato deverá ser adicionado à coleção canônica `semantic_classifications`, com `rule_id`, versão de regra, `semantic_type` igual a `target_or_forecast_candidate`, confiança `0.75`, evidência agregada e pergunta humana bloqueante. A saída não poderá carregar cabeçalho, valores, fórmulas, período, unidade, moeda ou contexto de negócio. A ausência de candidato não deverá gerar tipagem negativa.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| `Meta` com 10 ou mais números físicos finitos | candidato de meta ou previsto |
| `Orçado` com 10 ou mais números físicos finitos | candidato de meta ou previsto |
| `Forecast` com 10 ou mais números físicos finitos | candidato de meta ou previsto |
| Cabeçalho fora do vocabulário, mesmo com números físicos | sem candidato |
| Base de 9 números físicos finitos | sem candidato |
| Fórmula presente | sem candidato |
| Número armazenado como texto ou ambíguo | sem candidato |
| Data genericamente reconhecida | sem candidato |

## Bloqueio

Não há perfil, classificador, registro, versão de contrato, integração de pipeline, testes executáveis, dataset golden, calibração ou allowlist autorizados enquanto o gate de reconstrução não for aprovado por Chris.
