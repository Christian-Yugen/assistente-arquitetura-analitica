# GOLDEN-DATASET-CALIBRATION-001 — Calibração das Regras Executáveis Draft

**Decisão:** calibrado para regressão controlada no perfil draft.  
**Produção:** bloqueada.  
**Dataset:** `GD-QUALITY-DRAFT-001`, versão `1.0.0-draft`.

O dataset golden utiliza apenas perfis agregados sintéticos e determinísticos. Ele não contém valores de células, títulos originais de abas ou dados pessoais. Seu objetivo é preservar o comportamento esperado das regras autorizadas atualmente, e não representar uma amostra estatística de produção.

| Regra | Verdadeiros positivos | Falsos positivos | Falsos negativos | Cenários cobertos |
|---|---:|---:|---:|---|
| `QLT-NUMTEXT-007` | 4 | 0 | 0 | Baixo, médio com ambiguidade, alto, exclusão numérica e interação. |
| `QLT-NULL-001` | 4 | 0 | 0 | Baixo estrutural, médio vazio, alto `NaN`, exclusão de coluna vazia e interação. |

Os nove cenários concluíram sem divergência entre as assinaturas esperadas e as saídas do pipeline. Os cenários de exclusão não produziram finding, enquanto o cenário conjunto preservou os dois findings de alta severidade e suas perguntas de validação.

| Artefato | Controle |
|---|---|
| `artifacts/golden/quality-draft-golden-v1.json` | Fixture agregada de nove cenários. |
| `artifacts/golden/quality-draft-golden-v1.manifest.json` | SHA-256 `e8609d75a6d51bb838c2b48fff2a84cead9e582f8cfd1d87909a92b5eff2ad92`. |
| `artifacts/golden/quality-draft-golden-v1.calibration.json` | Relatório reprodutível `CAL-QUALITY-DRAFT-001`. |
| `engine/calibration/evaluate_quality_draft_golden.py` | Avaliador determinístico de assinaturas esperadas e observadas. |
| `engine/tests/test_golden_quality_draft.py` e `test_golden_quality_calibration.py` | Regressões da fixture, do hash e das métricas. |

> O resultado de zero desvio é restrito à fixture controlada. Ele não altera os limiares governados, não libera novas regras, não substitui dados reais de calibração supervisionada e não autoriza promoção produtiva.

O gate histórico `G7.5-QLT-NUMTEXT-007` não é reaberto automaticamente por este documento: sua exigência de recuperação canônica da QLT-NULL-001 permanece historicamente não atendida. A QLT-NULL-001 reconstruída foi aprovada somente pelo gate independente `QLT-NULL-RECONSTRUCTION-001`.
