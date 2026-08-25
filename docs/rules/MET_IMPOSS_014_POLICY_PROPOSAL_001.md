# MET-IMPOSS-014 — Proposta A de Política 001

## Escopo proposto

A `MET-IMPOSS-014` poderá, em um ciclo futuro e exclusivamente em draft, emitir um **alerta conceitual de suficiência insuficiente** quando não houver base agregada e não sensível para propor uma métrica revisável. O alerta não é uma métrica calculada, não afirma que dados de negócio estejam errados e exige decisão humana sobre a existência, a finalidade e a unidade de uma medida.

## Condição conservadora proposta

Uma futura implementação somente poderá emitir `metric_insufficient_review_required` se houver exatamente uma granularidade definida, nenhuma classificação indefinida ou conflito, nenhum fato sem grão, nenhum sinal de sensibilidade ou fórmula e contagem agregada de candidatos de medida igual a zero. A evidência deverá se limitar a flags e contagens agregadas; nomes de campos, títulos de abas, valores, posições, frequências e identificadores não podem compor a regra, a saída ou logs.

## Exclusões e bloqueios

Sensibilidade, fórmulas, granularidade ausente ou ambígua, classificação indefinida, fato sem grão, conflito, sinal de medida múltiplo, ou qualquer insuficiência de contexto bloqueiam o alerta. A regra não pode transformar ausência de sinal em diagnóstico de negócio, selecionar entidade, campo, unidade, população, período, filtro, agregação ou limiar.

## Saída permitida e decisão humana

Uma possível saída é apenas um finding conceitual, com confiança máxima de `0.55`, evidência agregada e pergunta bloqueante: “Existe uma medida de negócio apropriada para esta granularidade e qual é sua unidade e finalidade?”. A regra não calcula valores, não cria métrica, não recomenda fórmula e não gera DAX ou Power Query.

## Limite de autorização

Esta Proposta A não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção. A implementação exige autorização explícita e específica de Chris, em branch de segurança, depois de nova confirmação do critério técnico e de privacidade.
