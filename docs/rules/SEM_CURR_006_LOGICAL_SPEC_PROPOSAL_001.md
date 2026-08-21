# SEM-CURR-006 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris.

## Perfil privado proposto

O perfil por coluna deverá conter somente `physical_type`, `formula_count`, `header_eligible`, `physical_numeric_count`, `currency_format_numeric_count`, `numeric_text_candidate_count`, `numeric_text_ambiguity_count` e o sinal agregado da classificação de data. A normalização de cabeçalho usará NFKC, `casefold`, remoção de acentos e colapso de espaços durante o profiling; a inspeção de formato lerá cada formato de célula somente durante o profiling e o reduzirá a uma contagem. Nem cabeçalho normalizado, formato, marcador de moeda, código, valores, posições, título de aba, hash ou identificadores poderão ser persistidos.

## Condição determinística proposta

1. Exigir `header_eligible == true` para o vocabulário fechado definido na Proposta A.
2. Exigir `physical_type == "numeric"`.
3. Exigir `physical_numeric_count >= 10`.
4. Exigir `currency_format_numeric_count == physical_numeric_count`, para garantir formatação monetária explícita em todos os números físicos elegíveis.
5. Exigir `formula_count == 0`.
6. Exigir `numeric_text_candidate_count == 0` e `numeric_text_ambiguity_count == 0`.
7. Exigir ausência de candidato `date_generic` emitido pela SEM-DATE-001 para a mesma coluna.
8. Emitir `currency_candidate` somente quando todas as condições forem satisfeitas.

## Saída canônica proposta

O candidato deverá ser adicionado à coleção canônica `semantic_classifications`, com `rule_id`, versão de regra, `semantic_type` igual a `currency_candidate`, confiança `0.80`, evidência agregada e pergunta humana bloqueante. A saída não poderá carregar a moeda, símbolo, formato, cabeçalho ou valores que originaram os contadores. A ausência de candidato não deverá gerar tipagem negativa.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| `Receita` com 10 ou mais números físicos em formato `R$` | candidato monetário |
| `preco unitario` com 10 ou mais números físicos em formato `$` | candidato monetário |
| Cabeçalho fora do vocabulário, mesmo com formato de moeda | sem candidato |
| Base de 9 números físicos elegíveis | sem candidato |
| Um número físico em formato geral ou percentual | sem candidato |
| Fórmula presente | sem candidato |
| Número armazenado como texto ou ambíguo | sem candidato |
| Data genericamente reconhecida | sem candidato |

## Bloqueio

Não há perfil, classificador, registro, versão de contrato, integração de pipeline, testes executáveis, dataset golden, calibração ou allowlist autorizados enquanto o gate de reconstrução não for aprovado por Chris.
