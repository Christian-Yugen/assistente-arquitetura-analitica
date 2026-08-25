# REL-MANYMANY-004 — Gate Individual de Calibração Draft 001

## Escopo do gate

Este gate avalia exclusivamente a promoção da `REL-MANYMANY-004` ao perfil `executable_draft`. Ele não autoriza produção, criação de relações, tabelas ponte, direção de filtro, modificação de Power BI, alteração de dados ou execução de DAX/Power Query.

## Evidência verificável

| Item | Resultado |
|---|---|
| Dataset | `GD-REL-MANYMANY-004-001`, exclusivamente sintético. |
| Manifesto SHA-256 | `63ee7b1ed9eab8eb06b9928315f12fcf693da605f965053b7620871e6da7add9`. |
| Avaliador | `engine/calibration/evaluate_rel_manymany_draft_golden.py`. |
| Verdadeiros positivos | 3. |
| Falsos positivos | 0. |
| Falsos negativos | 0. |
| Saída | Somente `many_to_many_relationship_candidate`, confiança 0,75, severidade `warning` e pergunta bloqueante. |

## Controles preservados

O classificador recebe somente perfil agregado por par opaco. Títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores e fórmulas não alcançam o perfil persistível, evidências, contrato ou logs. Mascaramento, `SEM-SENS-015` e `sensitivity_classifications` permanecem controles independentes e bloqueiam a hipótese.

Fórmulas, sensibilidade, incompletude, cobertura parcial ou zero, 1:1, autorreferência, dimensão calendário, fato sem granularidade, classificação indefinida, conflito e ambiguidade bloqueiam a emissão. A não unicidade de ambos os lados não confirma por si só relacionamento muitos-para-muitos nem recomenda tabela ponte.

## Decisão

Com a Proposta A, o gate de reconstrução, a autorização específica de implementação de Chris, os testes e a calibração acima, a regra está apta somente à promoção controlada para `executable_draft`. A produção permanece bloqueada.
