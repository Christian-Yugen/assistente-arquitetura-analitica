# QLT-WHITESPACE-009-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-WHITESPACE-009 — Espaços e caracteres ocultos`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-WHITESPACE-009-RECONSTRUCTION-AUTHORIZATION-001`, com Opção A aprovada por Chris. | Aprovado. |
| Perfil privado | `WhitespaceProfile` contém somente contagens, proporção e base de normalização. | Aprovado. |
| Sinais limitados | Somente `U+0020`, `U+00A0`, `U+200B`, `U+200C`, `U+200D`, `U+2060` e `U+FEFF` participam da avaliação autorizada. | Aprovado. |
| Não intervenção | O avaliador não limpa, substitui, apara, normaliza, exclui ou reordena células. | Aprovado. |
| Golden dataset | `GD-QLT-WHITESPACE-009-001`, agregado e sem dados brutos, SHA-256 `f340b66558470ec7418e89fe11e45ff7259a26cc0ba9c76a88885f598ca295af`. | Aprovado. |
| Calibração | `CAL-QLT-WHITESPACE-009-001`: 3 TP, 0 FP, 0 FN em seis cenários. | Aprovado para draft. |
| Privacidade | Testes impedem a emissão de valores, posições, nomes de coluna e títulos de aba. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza tabulações, quebras de linha, controles genéricos, normalização Unicode, limpeza automática, uso produtivo, calibração em dados reais ou promoção do Gate MVP 1.0. As métricas cobrem somente o golden dataset agregado e não representam uma taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Toda ampliação do conjunto de caracteres ou do ambiente exige nova decisão humana e novo gate.
