# ALT-GRAIN-003 — Proposta A de Política 001

## Escopo proposto

A `ALT-GRAIN-003` poderá, em um ciclo futuro e exclusivamente em draft, consolidar um **bloqueio de granularidade indefinida** quando receber sinal de granularidade já inferido, opaco e agregado. Ela não inferirá grão a partir de headers, valores, posições, pares ou conteúdo privado e não afirmará qual deve ser a entidade, o evento, a chave ou o fato do modelo.

## Condição conservadora proposta

Uma futura implementação somente poderá emitir `undefined_grain_modeling_block` quando houver ao menos um sinal agregado de granularidade indefinida, nenhuma granularidade única confirmada e nenhum conflito de contrato. A saída poderá transportar apenas as contagens agregadas desses estados; ela não pode carregar identificação de aba, campo, candidato, valor, frequência, exemplos ou justificativa textual derivada do workbook.

## Exclusões e bloqueios

Ausência de sinal indefinido, granularidade única confirmada, conflito de contrato, estado ambíguo não qualificado ou qualquer tentativa de transportar identidade de workbook bloqueiam a emissão. A regra não seleciona entidades, fatos, dimensões, chaves, relacionamentos, medidas, períodos ou filtros; não calcula, altera, exclui, retém ou exporta dados e não gera DAX/M.

## Saída permitida e decisão humana

Uma possível saída é somente um finding conceitual de severidade alta e confiança máxima de `0.60`, acompanhado de pergunta humana bloqueante para confirmar a granularidade antes da modelagem. A decisão humana define a entidade, o evento, a chave e a unidade de análise sob governança.

## Limite de autorização

Esta Proposta A não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção. A implementação exige autorização explícita e específica de Chris, em branch de segurança. **Produção permanece bloqueada.**
