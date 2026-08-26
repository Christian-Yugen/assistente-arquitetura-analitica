# ALT-SUMPCT-007 — Gate de Reconstrução 001

## Decisão atual

Este gate aprovou inicialmente exclusivamente o intake `ALT-SUMPCT-007-INTAKE-001` e a `ALT_SUMPCT_007_POLICY_PROPOSAL_001.md` como documentação não executável, conforme `PROPOSAL-A-APPROVAL-DELEGATION-001`. Chris autorizou a implementação draft por chat: **“sim, aprovado vamos acelerar que eu quero colocar esse projeto em produção”**. A regra oficial é `ALT-SUMPCT-007 — Soma de percentuais`, no estágio `alert_consolidation`, escopo `model` e prioridade `P0`.

## Limite de uma implementação futura

Somente após autorização explícita de Chris, a implementação draft poderá consolidar uma contagem ou flag agregada de sinal independente de risco na soma de percentuais em uma pergunta humana de revisão. Ela não poderá detectar ou recomputar percentuais, somar ou comparar valores, inferir denominador, numerador, população, período, sobreposição, medida, campo, entidade, unidade, filtro, agregação, relação, fato ou dimensão. Ela não poderá usar ou expor dados privados nem gerar DAX/M.

## Bloqueios obrigatórios

Produção, promoção de ambiente e qualquer uso fora do perfil draft permanecem bloqueados. Perfil agregado, classificador, registry, contrato, pipeline, allowlist, testes executáveis, golden sintético, SHA-256, calibração TP/FP/FN e gate individual `ALT-SUMPCT-007-DRAFT-CALIBRATION-001` somente podem ser criados no escopo autorizado e devem preservar os controles deste gate. **Produção permanece bloqueada.**

## Próxima decisão necessária

O ciclo autorizado exige testes determinísticos, golden estritamente sintético, manifesto SHA-256, calibração TP/FP/FN, gate individual e allowlist draft antes de a regra ser executável. Sem todos esses controles, a execução é negada.
