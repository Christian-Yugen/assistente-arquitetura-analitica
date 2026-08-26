# ALT-AMBIG-005 — Proposta A de Política 001

## Escopo proposto

A `ALT-AMBIG-005` poderá, em um ciclo futuro e exclusivamente em draft, consolidar um **bloqueio de ambiguidade estrutural** a partir de sinais já inferidos, independentes, opacos e agregados. Ela não inferirá relações, caminhos, chaves ou granularidade a partir de headers, valores, posições, frequência, pares ou conteúdo privado e não decidirá uma solução de modelagem.

## Condição conservadora proposta

Uma futura implementação somente poderá emitir `structural_ambiguity_modeling_block` quando receber ao menos um sinal agregado de ambiguidade estrutural, nenhum relacionamento unívoco confirmado e nenhum conflito contratual. A saída poderá carregar somente as contagens agregadas desses estados; ela não pode transportar identificação de abas, tabelas, campos, caminhos, valores, candidatos ou justificativa derivada do workbook.

## Exclusões e bloqueios

Ausência de sinal de ambiguidade, relacionamento unívoco confirmado, conflito de contrato, sinal inconsistente ou qualquer risco de transportar identidade de workbook bloqueiam a emissão. A regra não seleciona relações, direções, chaves, fatos, dimensões, medidas, períodos ou filtros; não calcula, altera, exclui, retém ou exporta dados e não gera DAX/M.

## Saída permitida e decisão humana

Uma possível saída é somente um finding de severidade alta, confiança máxima de `0.60` e pergunta humana bloqueante para confirmar a estrutura antes da modelagem. A decisão humana define relações, direções e dependências sob governança.

## Limite de autorização

Esta Proposta A não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção. A implementação exige autorização explícita e específica de Chris, em branch de segurança. **Produção permanece bloqueada.**
