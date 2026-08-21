# QLT-OUTLIER-012-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-OUTLIER-012 — Valores atípicos`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-OUTLIER-012-RECONSTRUCTION-AUTHORIZATION-001`, com a Proposta A aprovada por Chris. | Aprovado. |
| Perfil privado | `OutlierProfile` mantém elegibilidade e contagens agregadas; não mantém valores, quartis, cercas, cabeçalhos, fórmulas, posições ou títulos de aba. | Aprovado. |
| Método fechado | Quartis lineares e cercas Tukey `Q1 − 1,5 × IQR` e `Q3 + 1,5 × IQR`, sem fallback estatístico. | Aprovado. |
| Elegibilidade e exclusões | Exige pelo menos 20 números físicos finitos, participação numérica mínima de 80% e `IQR` diferente de zero; números em texto, fórmulas, datas, booleanos, erros e não finitos são excluídos. | Aprovado. |
| Não intervenção | O avaliador não remove, corrige, substitui, arredonda, winsoriza, transforma, move ou reordena dados. | Aprovado. |
| Golden dataset | `GD-QLT-OUTLIER-012-001`, agregado e sem conteúdo bruto, SHA-256 `af197507e12f8d8b863566360a0322ae2d6dae361d9198754fd64f97d66a12a8`. | Aprovado. |
| Calibração | `CAL-QLT-OUTLIER-012-001`: 3 TP, 0 FP, 0 FN em oito cenários, incluindo severidades, ausência de candidatos, `IQR = 0`, base insuficiente, participação numérica baixa e base não autorizada. | Aprovado para draft. |
| Validação humana | Todo finding emite pergunta humana não bloqueante; extremo estatístico não é tratado como erro confirmado. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza z-score, MAD, aprendizado de máquina, métodos alternativos quando `IQR = 0`, agrupamento, segmentação, sazonalidade, comparação entre colunas, inferência de domínio, correção automática ou uso produtivo. As métricas cobrem somente o golden dataset agregado e não representam taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Qualquer alteração de método, base, limiar, escopo ou ambiente exige nova decisão humana, novas evidências e novo gate.
