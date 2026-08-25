# ALT-SENS-001 — Proposta A de Política 001

## Escopo proposto

A `ALT-SENS-001` poderá, em um ciclo futuro e exclusivamente em draft, consolidar um alerta de **restrição de processamento** quando já existir exatamente um sinal independente de sensibilidade. Ela não reconhecerá, classificará, nomeará, exibirá ou deduzirá nenhum dado pessoal a partir de cabeçalhos, valores, formatos, pares, posições, títulos ou conteúdo de workbook.

## Condição conservadora proposta

Uma futura implementação somente poderá emitir `sensitive_data_processing_restriction` quando receber um único sinal de sensibilidade pré-classificado, opaco e agregado, sem conflito de classificação. A saída deve conter apenas a contagem agregada do sinal e uma instrução de controle; não pode transportar a classe específica, exemplos, frequência, valor ou identidade da coluna.

## Exclusões e bloqueios

Ausência ou multiplicidade de sinais, conflito de classificação, classificação indefinida, perfil inconsistente, falha de contrato ou qualquer risco de transportar identidade de campo bloqueiam a emissão. A regra não altera, apaga, mascara, retém, exporta, envia ou desbloqueia dados; ela não cria DAX/M, nem recomenda processamento adicional.

## Saída permitida e decisão humana

Uma possível saída é somente um finding `sensitive_data_processing_restriction`, de severidade alta e confiança máxima de `0.60`, com orientação humana bloqueante para interromper o uso da coluna na modelagem até revisão adequada. A decisão humana confirma a restrição, o encaminhamento de privacidade e a eventual necessidade de exclusão ou mascaramento sob processo aprovado.

## Limite de autorização

Esta Proposta A não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção. A implementação exige autorização explícita e específica de Chris, em branch de segurança. **Produção permanece bloqueada.**
