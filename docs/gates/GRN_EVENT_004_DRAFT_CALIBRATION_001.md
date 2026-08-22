# GRN-EVENT-004 — Gate de Calibração Draft 001

## Decisão

A `GRN-EVENT-004@0.1.0-provisional.1` está autorizada para execução **exclusivamente no perfil draft**. A ativação decorre da Proposta A aprovada por Chris, do gate de reconstrução `GRN-EVENT-004-RECONSTRUCTION-AUTHORIZATION-001`, da autorização explícita para implementação draft e das evidências reproduzíveis registradas abaixo.

## Evidência de calibração

| Campo | Resultado |
|---|---|
| Golden dataset | `GD-GRN-EVENT-004-001` |
| Caminho | `artifacts/golden/grn-event-draft-golden-v1.json` |
| SHA-256 | `6ef71effd44ea955f96f434d15437242d1e45ce18dc9d43d3d12a9b9809e019a` |
| Avaliador | `python3 -m engine.calibration.evaluate_grn_event_draft_golden` |
| Verdadeiros positivos | 3 |
| Falsos positivos | 0 |
| Falsos negativos | 0 |

Resultado consolidado do avaliador: `{"true_positives": 3, "false_positives": 0, "false_negatives": 0}`.

O golden dataset contém somente contagens agregadas sintéticas, sem valores de planilha, cabeçalhos, identificadores reais, posições, títulos de aba, dados pessoais ou frequências por rótulo. O avaliador retorna apenas as contagens TP/FP/FN.

## Limites preservados

A regra exige pelo menos 20 linhas, exatamente um marcador fechado de evento elegível, exatamente uma hipótese previamente emitida pela GRN-EXPL-002 e exatamente uma data reconhecida que não seja competência. Fórmulas, sinais excluídos ou qualquer ambiguidade bloqueiam a emissão. A saída é a hipótese `event_per_row_candidate`, com confiança `0.80` e confirmação humana bloqueante.

Não há confirmação de evento de negócio, classificação automática de fato, criação de relacionamento, inferência de métrica ou divulgação de cabeçalho, valores, posição ou título de aba. Produção permanece bloqueada.

## Condição de regressão

Qualquer mudança de vocabulário, base mínima, exclusão, dependência da chave explícita, reconhecimento temporal, contrato, profiler, classificador, pipeline ou evidência exige nova proposta, aprovação explícita de Chris, nova calibração e novo gate.
