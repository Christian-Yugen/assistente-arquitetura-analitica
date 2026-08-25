# ALT-QUALITY-002 — Proposta A de Política 001

## Escopo proposto

A `ALT-QUALITY-002` poderá, em um ciclo futuro e exclusivamente em draft, consolidar um **risco crítico de qualidade** a partir de findings de qualidade já executados e reduzidos a contagens agregadas. Ela não reexecutará regras de qualidade, não inferirá defeitos novos, não calculará valores e não exibirá planilha, coluna, cabeçalho, valor, posição, frequência, pares ou identificadores.

## Condição conservadora proposta

Uma futura implementação somente poderá emitir `critical_quality_risk_review_required` quando houver ao menos três findings de qualidade de severidade alta e ao menos duas regras de qualidade distintas, ambos como contagens agregadas de fonte independente. A condição precisa de um modelo com ao menos uma aba analisada e nenhum erro contratual. A regra apenas consolida o risco técnico; não determina prioridade de negócio, causa-raiz, correção ou impacto financeiro.

## Exclusões e bloqueios

Ausência de contexto, menos de três findings altos, menos de duas regras distintas, inconsistência de contagem, erro de contrato ou qualquer tentativa de incluir identidade de workbook bloqueiam a emissão. A regra não altera, exclui, corrige, normaliza, retém ou exporta dados, não escolhe colunas, não classifica conteúdo e não gera DAX/M.

## Saída permitida e decisão humana

Uma possível saída é apenas um finding conceitual de severidade alta, com confiança máxima de `0.60`, evidência de contagens agregadas e pergunta humana bloqueante sobre a priorização da revisão de qualidade. A decisão humana define escopo, responsável, correção e eventual aceite de risco.

## Limite de autorização

Esta Proposta A não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção. A implementação exige autorização explícita e específica de Chris, em branch de segurança. **Produção permanece bloqueada.**
