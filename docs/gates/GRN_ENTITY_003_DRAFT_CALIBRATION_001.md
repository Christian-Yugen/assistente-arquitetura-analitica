# Gate de Calibração Draft — GRN-ENTITY-003

## Decisão

A `GRN-ENTITY-003@0.1.0-provisional.1` está autorizada para execução **exclusivamente no perfil draft**. A ativação decorre da Proposta A aprovada por Chris, do gate `GRN-ENTITY-003-RECONSTRUCTION-AUTHORIZATION-001`, da autorização explícita posterior para implementação draft e das evidências reproduzíveis registradas abaixo.

## Evidência de calibração

| Campo | Resultado |
|---|---|
| Golden dataset | `GD-GRN-ENTITY-003-001` |
| Caminho | `artifacts/golden/grn-entity-draft-golden-v1.json` |
| SHA-256 | `44b809ab2acf3bd8ba6353e1294ff17016df73dad5f5e11c26d19c2bf949e50e` |
| Avaliador | `python3 -m engine.calibration.evaluate_grn_entity_draft_golden` |
| Verdadeiros positivos | 3 |
| Falsos positivos | 0 |
| Falsos negativos | 0 |

Resultado consolidado do avaliador: `{"true_positives": 3, "false_positives": 0, "false_negatives": 0}`.

O golden dataset contém apenas contagens agregadas sintéticas, sem valores de planilha, cabeçalhos, identificadores reais, posições, títulos de aba, dados pessoais ou frequências por rótulo. O avaliador retorna apenas as contagens TP/FP/FN.

## Limites preservados

A regra exige pelo menos 20 linhas, exatamente um marcador fechado de entidade, exatamente uma hipótese prévia da GRN-EXPL-002 e pelo menos um atributo descritivo. Qualquer sinal de tempo não competência, evento, medida, sensibilidade, fórmula, marcador excluído ou ambiguidade bloqueia a emissão. A saída é a hipótese `entity_per_row_candidate`, com confiança `0.75` e confirmação humana bloqueante.

Não há confirmação de entidade de negócio, classificação automática de dimensão, criação de chave primária, SCD ou relacionamento, nem divulgação de cabeçalho, valores, posição ou título de aba. Produção permanece bloqueada.

## Condição de regressão

Qualquer mudança de vocabulário, base mínima, dependência de chave explícita, atributo descritivo, exclusões, contrato, profiler, classificador, pipeline ou evidência exige nova proposta, aprovação explícita de Chris, nova calibração e novo gate.
