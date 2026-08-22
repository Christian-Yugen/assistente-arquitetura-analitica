# GRN-EXPL-002 — Gate de Calibração Draft 001

## Decisão

A `GRN-EXPL-002@0.1.0-provisional.1` está autorizada para execução **exclusivamente no perfil draft**. A ativação decorre da Proposta A aprovada por Chris, do gate de reconstrução `GRN-EXPL-002-RECONSTRUCTION-AUTHORIZATION-001` e das evidências reproduzíveis registradas abaixo.

## Evidência de calibração

| Campo | Resultado |
|---|---|
| Golden dataset | `GD-GRN-EXPL-002-001` |
| Caminho | `artifacts/golden/grn-expl-draft-golden-v1.json` |
| SHA-256 | `ab368d7e0758c07ea0afd6974b5ac6c9335354c2346e1ab9bde27be546fc6b7a` |
| Avaliador | `python3 -m engine.calibration.evaluate_grn_expl_draft_golden` |
| Verdadeiros positivos | 3 |
| Falsos positivos | 0 |
| Falsos negativos | 0 |

Resultado consolidado do avaliador: `{"true_positives": 3, "false_positives": 0, "false_negatives": 0}`.

O golden dataset contém apenas metadados sintéticos e cabeçalhos técnicos, sem valores de planilha, identificadores reais, rótulos de dados, posição, título de aba ou dado pessoal. O avaliador retorna somente contagens TP/FP/FN.

## Limites preservados

A regra exige uma única coluna elegível com cabeçalho explícito fechado, classificação de identificador, pelo menos 20 linhas, cobertura e unicidade totais, zero fórmulas e nenhuma ambiguidade. A saída é uma hipótese `explicit_key_candidate`, com confiança `0.85` e confirmação humana bloqueante.

Não há confirmação de chave primária, criação de relacionamento, combinação de colunas, inferência de chave composta, divulgação de cabeçalho ou valores. Produção permanece bloqueada.

## Condição de regressão

Qualquer mudança de vocabulário, contagem mínima, completude, unicidade, exclusão, contrato, profiler, classificador, pipeline ou evidência exige nova proposta, aprovação explícita de Chris, nova calibração e novo gate.
