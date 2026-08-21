# SEM-QTY-005 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris.

## Perfil privado proposto

O perfil por coluna deverá conter somente `physical_type`, `formula_count`, `header_eligible`, `physical_numeric_count`, `numeric_text_candidate_count`, `numeric_text_ambiguity_count` e o sinal agregado de classificação de data. O cabeçalho será normalizado transitoriamente por NFKC, casefold, remoção de acentos e colapso de espaços; o texto normalizado não será persistido. Valores, posições, título de aba, hash e identificadores serão descartados.

## Condição determinística proposta

1. Exigir `header_eligible == true` para o vocabulário fechado `quantidade`, `qtd`, `qtde`.
2. Exigir `physical_type == "numeric"`.
3. Exigir `physical_numeric_count >= 10`.
4. Exigir `formula_count == 0`.
5. Exigir `numeric_text_candidate_count == 0` e `numeric_text_ambiguity_count == 0`.
6. Exigir ausência de candidato `date_generic` emitido pela SEM-DATE-001 para a mesma coluna.
7. Emitir `quantity_candidate` somente quando todas as condições forem satisfeitas.

## Saída canônica proposta

O candidato deverá ser adicionado à coleção canônica `semantic_classifications`, com `rule_id`, versão de regra, `semantic_type` igual a `quantity_candidate`, confiança `0.75`, evidência agregada e pergunta humana bloqueante. A ausência de candidato não deverá gerar tipagem negativa ou revelar o cabeçalho de origem.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| `Quantidade` com 10 ou mais números físicos finitos | candidato de quantidade |
| `qtd` ou `qtde` com números físicos | candidato de quantidade |
| Cabeçalho fora do vocabulário | sem candidato |
| Base de 9 números físicos | sem candidato |
| Número armazenado como texto | sem candidato |
| Número ambíguo como texto | sem candidato |
| Fórmula presente | sem candidato |
| Data genericamente reconhecida | sem candidato |

## Bloqueio

Não há perfil, classificador, registro, versão de contrato, integração de pipeline, testes executáveis, dataset golden, calibração ou allowlist autorizados enquanto o gate de reconstrução não for aprovado por Chris.
