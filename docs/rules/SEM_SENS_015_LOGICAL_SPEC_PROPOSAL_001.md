# SEM-SENS-015 — Especificação Lógica Proposta 001

**Estado:** não executável; depende da aprovação explícita da Proposta A por Chris.

## Perfil privado proposto

A implementação deverá reutilizar somente sinais privados já agregados do perfil de identificador: `sensitive_header` e `non_missing_count`. Nenhum novo accumulator poderá reter valor, formato, fórmula, posição, título de aba, domínio de e-mail, identificador, hash ou amostra de conteúdo. A elegibilidade do cabeçalho será calculada de forma transitória por normalização NFKC, `casefold`, remoção de acentos e colapso de espaços.

## Condição determinística proposta

1. Exigir `sensitive_header == true` para o vocabulário fechado definido na Proposta A.
2. Exigir `non_missing_count >= 1`.
3. Emitir `personal_data_candidate` no campo canônico `sensitivity` somente quando ambas as condições forem satisfeitas.
4. Não usar tipo físico, valor, fórmula, texto numérico, data, unicidade, distribuição ou contexto de outras colunas como evidência.
5. Não alterar o fluxo de mascaramento existente, independentemente de haver ou não candidato emitido.

## Saída canônica proposta

O candidato deverá ser adicionado ao campo canônico `sensitivity`, com `rule_id`, versão de regra, classificação `personal_data_candidate`, confiança `0.90`, evidência agregada e pergunta humana bloqueante. A saída não poderá carregar cabeçalho, valores, categoria de documento, formato, posição, aba, hash ou identificador. A ausência de candidato não reduzirá nem removerá proteções existentes.

## Matriz mínima de testes a autorizar posteriormente

| Cenário | Resultado esperado |
|---|---|
| Cabeçalho `CPF` e uma ou mais observações | candidato de dado pessoal |
| Cabeçalho `E-mail` e uma ou mais observações | candidato de dado pessoal |
| Cabeçalho `Nome` e uma ou mais observações | candidato de dado pessoal |
| Cabeçalho elegível sem observações | sem candidato |
| Cabeçalho `Cliente` com observações | sem candidato |
| Valores parecidos com PII sob cabeçalho inelegível | sem candidato; sem inspeção de valores |
| Coluna com fórmulas sob cabeçalho elegível | classificação independente de fórmula; mascaramento preservado |

## Bloqueio

Não há perfil, classificador, registro, versão de contrato, integração de pipeline, testes executáveis, dataset golden, calibração ou allowlist autorizados enquanto o gate de reconstrução não for aprovado por Chris.
