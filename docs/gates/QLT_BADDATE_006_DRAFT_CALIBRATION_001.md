# QLT-BADDATE-006-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-BADDATE-006 — Datas inválidas`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-BADDATE-006-RECONSTRUCTION-AUTHORIZATION-001`, com três formatos estritos aceitos por Chris. | Aprovado. |
| Perfil privado | `BadDateProfile` conserva apenas contagens, razão e base de normalização. | Aprovado. |
| Gramáticas limitadas | Apenas `AAAA-MM-DD`, `DD-MM-AAAA` e `DD/MM/AAAA` participam da avaliação. | Aprovado. |
| Não intervenção | O avaliador não converte, exclui, preenche ou reordena células. | Aprovado. |
| Golden dataset | `GD-QLT-BADDATE-006-001`, agregado e sem dados brutos, SHA-256 `149cd1d9d649917e6e25eaab26ffb6cbad44b7b4e50a8bfffba3daea9e067b11`. | Aprovado. |
| Calibração | `CAL-QLT-BADDATE-006-001`: 3 TP, 0 FP, 0 FN em seis cenários. | Aprovado para draft. |
| Privacidade | Testes impedem a emissão de valores, posições, nomes de coluna e títulos de aba. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza inferência de locale, parsing de outros formatos, tratamento de datas nativas ou seriais, correção automática, uso produtivo, calibração em dados reais ou promoção do Gate MVP 1.0. As métricas cobrem somente o golden dataset agregado e não representam uma taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Toda expansão para outra gramática ou ambiente exige nova decisão humana e novo gate.
