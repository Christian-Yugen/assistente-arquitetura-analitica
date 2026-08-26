# GRN-ASSOC-007 — Gate de reconstrução e autorização

**Regra:** `GRN-ASSOC-007 — Associação entre entidades`
**Decisão:** autorizada exclusivamente para **draft controlado**.
**Registro da autorização de implementação:** Chris — “autorizado”.

O ciclo foi autorizado após intake e Proposta A. O executor só consolida sinal **independente, autorizado, opaco e agregado** para formular uma hipótese de revisão humana. Ausência de sinal, confirmação humana prévia, conflito estrutural, sensibilidade ou erro contratual suprimem o finding de modo fail-closed.

A regra não infere, identifica, vincula, compara ou seleciona entidades, eventos, chaves, fatos, dimensões, relações, cardinalidades, campos, valores, pares, frequências, calendário ou conteúdo de workbook. Não persiste nem expõe conteúdo de workbook, não calcula métricas e não gera DAX ou Power Query. O pipeline real fixa o sinal independente em zero enquanto não existir fonte independente autorizada.

O gate individual `GRN-ASSOC-007-DRAFT-CALIBRATION-001`, o golden estritamente sintético, o manifesto SHA-256, os testes determinísticos, a allowlist e a regressão integral sustentam apenas o perfil draft. **Produção permanece bloqueada** até os requisitos próprios de cobertura, calibração produtiva, exclusão física, E2E e gate produtivo.
