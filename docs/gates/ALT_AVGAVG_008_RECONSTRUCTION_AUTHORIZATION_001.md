# ALT-AVGAVG-008 — Gate de Reconstrução 001

## Decisão atual

Este gate aprova exclusivamente o intake `ALT-AVGAVG-008-INTAKE-001` e a `ALT_AVGAVG_008_POLICY_PROPOSAL_001.md` como documentação não executável, conforme `PROPOSAL-A-APPROVAL-DELEGATION-001`. A regra oficial é `ALT-AVGAVG-008 — Média de médias`, no estágio `alert_consolidation`, escopo `model` e prioridade `P0`.

## Limite de uma implementação futura

Somente após autorização explícita de Chris, a implementação draft poderá consolidar uma contagem ou flag agregada de sinal independente de risco em média de médias em uma pergunta humana de revisão. Ela não poderá detectar, recomputar, ponderar, comparar ou calcular médias, nem inferir peso, denominador, população, período, medida, campo, entidade, unidade, filtro, agregação, relação, fato ou dimensão. Ela não poderá usar ou expor dados privados nem gerar DAX/M.

## Bloqueios obrigatórios

Perfil agregado, classificador, registry, contrato, pipeline, allowlist, testes executáveis, golden sintético, SHA-256, calibração TP/FP/FN e gate individual `ALT-AVGAVG-008-DRAFT-CALIBRATION-001` ainda não existem. A regra não é executável e não altera a contagem do workspace. **Produção permanece bloqueada.**

## Próxima decisão necessária

Chris deve autorizar explicitamente a criação de código executável para esta regra no perfil draft. Sem essa autorização, a execução é negada e nenhum comportamento do motor pode ser modificado.
