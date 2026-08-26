# GRN-PREAGG-008 — Gate de reconstrução e autorização

**Regra:** `GRN-PREAGG-008 — Agregação prévia`
**Decisão:** autorizada exclusivamente para **draft controlado**.
**Registro da autorização de implementação:** Chris — “autorizado”.

O executor somente consolida sinal **independente, autorizado, opaco e agregado** para hipótese de revisão humana. Ausência de sinal, confirmação humana prévia, conflito estrutural, sensibilidade ou erro contratual suprimem o finding de modo fail-closed. A regra não infere, identifica, calcula, soma, conta, compara, recomputa, seleciona ou desagrega métricas, medidas, níveis de detalhe, entidades, eventos, chaves, fatos, dimensões, relações, cardinalidades, campos, valores, frequências, períodos ou conteúdo de workbook. O pipeline real fixa o sinal independente em zero enquanto não existir fonte independente autorizada.

Golden sintético, SHA-256, testes, allowlist e gate individual sustentam somente draft. **Produção permanece bloqueada** até cobertura, calibração produtiva, exclusão física, E2E e gate produtivo.
