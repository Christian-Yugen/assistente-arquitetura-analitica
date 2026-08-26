# ALT-AVGAVG-008 — Gate de Reconstrução 001

## Decisão atual

Este gate aprovou inicialmente exclusivamente o intake `ALT-AVGAVG-008-INTAKE-001` e a `ALT_AVGAVG_008_POLICY_PROPOSAL_001.md` como documentação não executável, conforme `PROPOSAL-A-APPROVAL-DELEGATION-001`. Chris autorizou a implementação draft por chat: **“dim, autorizado”**. A regra oficial é `ALT-AVGAVG-008 — Média de médias`, no estágio `alert_consolidation`, escopo `model` e prioridade `P0`.

## Limite de uma implementação futura

Somente após autorização explícita de Chris, a implementação draft poderá consolidar uma contagem ou flag agregada de sinal independente de risco em média de médias em uma pergunta humana de revisão. Ela não poderá detectar, recomputar, ponderar, comparar ou calcular médias, nem inferir peso, denominador, população, período, medida, campo, entidade, unidade, filtro, agregação, relação, fato ou dimensão. Ela não poderá usar ou expor dados privados nem gerar DAX/M.

## Bloqueios obrigatórios

Produção, promoção de ambiente e qualquer uso fora do perfil draft permanecem bloqueados. Perfil agregado, classificador, registry, contrato, pipeline, allowlist, testes executáveis, golden sintético, SHA-256, calibração TP/FP/FN e gate individual `ALT-AVGAVG-008-DRAFT-CALIBRATION-001` somente podem ser criados no escopo autorizado e devem preservar os controles deste gate. **Produção permanece bloqueada.**

## Próxima decisão necessária

O ciclo autorizado exige testes determinísticos, golden estritamente sintético, manifesto SHA-256, calibração TP/FP/FN, gate individual e allowlist draft antes de a regra ser executável. Sem todos esses controles, a execução é negada.
