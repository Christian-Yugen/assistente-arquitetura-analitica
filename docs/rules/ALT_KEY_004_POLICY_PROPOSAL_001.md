# ALT-KEY-004 — Proposta A de Política 001

## Escopo proposto

A `ALT-KEY-004` poderá, em um ciclo futuro e exclusivamente em draft, consolidar um **bloqueio de chave inválida** a partir de sinais de chave já inferidos, independentes, opacos e agregados. Ela não detectará chaves pela leitura de headers, valores, posições, frequência, exemplos, pares ou conteúdo privado e não declarará qual campo deve ser uma chave do modelo.

## Condição conservadora proposta

Uma futura implementação somente poderá emitir `invalid_key_modeling_block` quando receber ao menos um sinal agregado de chave inválida, nenhum sinal de chave confirmada e nenhum conflito contratual. A saída poderá carregar somente as contagens agregadas dos sinais; ela não pode transportar identificação de abas, tabelas, campos, candidatos, valores, duplicidades individuais ou justificativa derivada do workbook.

## Exclusões e bloqueios

Ausência de sinal inválido, chave confirmada, conflito de contrato, sinal ambíguo ou qualquer risco de transportar identidade de workbook bloqueiam a emissão. A regra não seleciona chaves, fatos, dimensões, relacionamentos, medidas ou filtros; não calcula, altera, exclui, retém ou exporta dados e não gera DAX/M.

## Saída permitida e decisão humana

Uma possível saída é somente um finding de severidade alta, confiança máxima de `0.60` e pergunta humana bloqueante para confirmar a chave válida antes da modelagem. A decisão humana define a chave, o escopo e a política de integridade sob governança.

## Limite de autorização

Esta Proposta A não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção. A implementação exige autorização explícita e específica de Chris, em branch de segurança. **Produção permanece bloqueada.**
