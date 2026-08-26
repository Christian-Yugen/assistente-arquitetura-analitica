# GRN-SNAP-006 — Gate de reconstrução e autorização

**Regra:** `GRN-SNAP-006 — Snapshot periódico`
**Decisão:** autorizada exclusivamente para **draft controlado**.
**Registro da autorização de implementação:** Chris — “sim”.

O ciclo foi autorizado após intake e Proposta A. O executor só consolida um sinal **independente, autorizado, opaco e agregado** para formular uma hipótese de revisão humana. Ausência de sinal, confirmação humana prévia, conflito estrutural, sensibilidade ou erro contratual suprimem o finding de forma fail-closed.

A regra não infere periodicidade, calendário, entidade, evento, chave, fato, dimensão, relação, medida, campo, valor ou conteúdo privado. Não persiste nem expõe conteúdo de workbook, não calcula métricas e não gera DAX ou Power Query. O pipeline real fixa o sinal independente em zero enquanto não existir fonte independente autorizada.

O gate individual `GRN-SNAP-006-DRAFT-CALIBRATION-001`, o golden estritamente sintético, o manifesto SHA-256, os testes determinísticos, a allowlist e a regressão integral sustentam apenas o perfil draft. **Produção permanece bloqueada** até os requisitos próprios de cobertura, calibração produtiva, exclusão física, E2E e gate produtivo.
