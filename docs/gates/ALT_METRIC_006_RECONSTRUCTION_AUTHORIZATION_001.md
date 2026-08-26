# ALT-METRIC-006 — Gate de Reconstrução 001

## Decisão atual

O gate aprova exclusivamente o intake `ALT-METRIC-006-INTAKE-001` e a `ALT_METRIC_006_POLICY_PROPOSAL_001.md` como documentação não executável, conforme `PROPOSAL-A-APPROVAL-DELEGATION-001`. A regra oficial é `ALT-METRIC-006 — Métrica potencialmente enganosa`, no estágio `alert_consolidation`, escopo `model` e prioridade `P0`.

## Limite da futura implementação

Após autorização explícita e específica de Chris, uma eventual implementação draft poderá somente consolidar sinais já produzidos por fonte independente, autorizada, opaca e agregada em uma solicitação de revisão humana. Não poderá inferir risco a partir de conteúdo privado nem declarar uma métrica, decisão ou resultado de negócio como incorreto. Ela não poderá calcular, escolher ou nomear medida, campo, entidade, unidade, população, período, filtro, agregação, relação, fato ou dimensão; não poderá gerar DAX/M, editar, excluir, reter ou exportar dados.

## Bloqueios obrigatórios

Perfil agregado, classificador, registry, contrato, pipeline, allowlist, testes executáveis, golden sintético, SHA-256, calibração TP/FP/FN e gate individual `ALT-METRIC-006-DRAFT-CALIBRATION-001` ainda não existem e permanecem bloqueados. A entrada `ALT-METRIC-006` não é executável e não altera a contagem do workspace. **Produção permanece bloqueada.**

## Próxima decisão necessária

Chris deve autorizar explicitamente a criação de código executável para a regra no perfil draft. Sem essa autorização, a execução é negada e nenhum comportamento do motor pode ser modificado.
