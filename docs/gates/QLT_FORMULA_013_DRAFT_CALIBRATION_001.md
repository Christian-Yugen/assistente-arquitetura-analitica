# QLT-FORMULA-013-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-FORMULA-013 — Fórmulas inconsistentes`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-FORMULA-013-RECONSTRUCTION-AUTHORIZATION-001`, com a Proposta A aprovada por Chris. | Aprovado. |
| Perfil privado | `FormulaConsistencyProfile` mantém somente contagens e razão; não mantém fórmulas, referências, valores calculados, cabeçalhos, posições ou títulos de aba. | Aprovado. |
| Sinal fechado | A regra compara apenas presença versus ausência de tipo de célula `f`; não lê nem compara o conteúdo das expressões. | Aprovado. |
| Elegibilidade e exclusões | Exige 10 células físicas não vazias, 8 fórmulas e participação mínima de 80%; células vazias, bases insuficientes e comparação entre expressões são excluídas. | Aprovado. |
| Não intervenção | O avaliador não cria, copia, corrige, preenche, apaga, recalcula, move ou reordena fórmulas ou valores. | Aprovado. |
| Golden dataset | `GD-QLT-FORMULA-013-001`, agregado e sem conteúdo bruto, SHA-256 `dc18f7e4a1f912fc97627df975780cd771971586a39cecbbce1e9f09b9ca5e61`. | Aprovado. |
| Calibração | `CAL-QLT-FORMULA-013-001`: 3 TP, 0 FP, 0 FN em seis cenários, incluindo severidades, ausência de substituição manual, base insuficiente e baixa participação de fórmulas. | Aprovado para draft. |
| Validação humana | Todo finding emite pergunta humana não bloqueante; presença de valor manual não é tratada como erro confirmado. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza leitura ou normalização de expressões, comparação entre fórmulas, avaliação de referências, recálculo de workbook, fórmulas automáticas, cópia de fórmulas, identificação de fórmulas matematicamente diferentes, transformação automática ou uso produtivo. As métricas cobrem somente o golden dataset agregado e não representam taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Qualquer alteração de sinal, acesso a expressão, base, limiar, escopo ou ambiente exige nova decisão humana, novas evidências e novo gate.
