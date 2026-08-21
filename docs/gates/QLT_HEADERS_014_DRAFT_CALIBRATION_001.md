# QLT-HEADERS-014-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-HEADERS-014 — Cabeçalhos inválidos`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-HEADERS-014-RECONSTRUCTION-AUTHORIZATION-001`, com a Proposta A aprovada por Chris. | Aprovado. |
| Perfil privado | `HeadersProfile` mantém somente contagens agregadas; não mantém textos, títulos de abas, posições, endereços, ranges, fórmulas ou valores. | Aprovado. |
| Sinais fechados | A regra observa apenas ausência na primeira linha, duplicidade textual normalizada e candidato multinível por mesclagem horizontal iniciada na primeira linha. | Aprovado. |
| Exclusões | Cabeçalhos posteriores, estilos, cores, comentários, fórmulas, semântica, ranges fora da primeira linha e correções automáticas são excluídos. | Aprovado. |
| Não intervenção | O avaliador não renomeia, preenche, deduplica, desmescla, move, exclui, insere ou reordena células, linhas, colunas ou abas. | Aprovado. |
| Golden dataset | `GD-QLT-HEADERS-014-001`, agregado e sem conteúdo bruto, SHA-256 `db2e2143c60d3c83c816aef20479c775dbf307ddb480b0ba4e4568f71d3fe87a`. | Aprovado. |
| Calibração | `CAL-QLT-HEADERS-014-001`: 3 TP, 0 FP, 0 FN em seis cenários, incluindo ausência, duplicidade normalizada, candidato multinível, ausência de sinais e perfis inválidos. | Aprovado para draft. |
| Validação humana | Todo finding emite pergunta humana; a confirmação da estrutura correta é sempre humana. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza buscar outra linha de cabeçalho, inferir nomes semânticos, comparar títulos de abas, inspecionar estilos, converter candidato multinível em erro confirmado, alterar mesclagens ou corrigir automaticamente a estrutura. As métricas cobrem somente o golden dataset agregado e não representam taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Qualquer alteração de sinal, linha de referência, evidência, escopo ou ambiente exige nova decisão humana, novas evidências e novo gate.
