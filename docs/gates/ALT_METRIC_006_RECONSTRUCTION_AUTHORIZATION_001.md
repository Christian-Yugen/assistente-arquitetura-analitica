# ALT-METRIC-006 — Gate de Reconstrução 001

## Decisão atual

O gate aprovou inicialmente exclusivamente o intake `ALT-METRIC-006-INTAKE-001` e a `ALT_METRIC_006_POLICY_PROPOSAL_001.md` como documentação não executável, conforme `PROPOSAL-A-APPROVAL-DELEGATION-001`. Chris autorizou a implementação draft por chat: **“sim autorizado. continue isso logo para finaizarmos essas 95 regras”**. A regra oficial é `ALT-METRIC-006 — Métrica potencialmente enganosa`, no estágio `alert_consolidation`, escopo `model` e prioridade `P0`.

## Limite da futura implementação

Após autorização explícita e específica de Chris, uma eventual implementação draft poderá somente consolidar sinais já produzidos por fonte independente, autorizada, opaca e agregada em uma solicitação de revisão humana. Não poderá inferir risco a partir de conteúdo privado nem declarar uma métrica, decisão ou resultado de negócio como incorreto. Ela não poderá calcular, escolher ou nomear medida, campo, entidade, unidade, população, período, filtro, agregação, relação, fato ou dimensão; não poderá gerar DAX/M, editar, excluir, reter ou exportar dados.

## Bloqueios obrigatórios

Produção, promoção de ambiente e qualquer uso fora do perfil draft permanecem bloqueados. O perfil agregado, classificador, registry, contrato, pipeline, allowlist, testes executáveis, golden sintético, SHA-256, calibração TP/FP/FN e gate individual `ALT-METRIC-006-DRAFT-CALIBRATION-001` somente podem ser criados dentro do escopo autorizado e devem manter os controles descritos neste gate. **Produção permanece bloqueada.**

## Próxima decisão necessária

O ciclo autorizado exige testes determinísticos, golden estritamente sintético, manifesto SHA-256, calibração com TP/FP/FN, gate individual e allowlist draft antes de a regra ser considerada executável. Sem todos esses controles, a execução é negada.
