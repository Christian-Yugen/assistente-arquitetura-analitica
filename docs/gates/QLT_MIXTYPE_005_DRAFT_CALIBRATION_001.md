# QLT-MIXTYPE-005-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-MIXTYPE-005 — Tipos mistos`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política aprovada | `QLT-MIXTYPE-005-RECONSTRUCTION-AUTHORIZATION-001`, com Opção A aceita por Chris. | Aprovado. |
| Perfil privado | `MixedTypesProfile` contém somente contagens por grupo físico e base de normalização. | Aprovado. |
| Não intervenção | O avaliador não converte, exclui, preenche ou reordena células. | Aprovado. |
| Separação de regra | Cadeias numéricas canônicas são delegadas à QLT-NUMTEXT-007. | Aprovado. |
| Golden dataset | `GD-QLT-MIXTYPE-005-001`, agregado e sem valores brutos, SHA-256 `385134ca760f35d4239cb0c1e9910b16abe1eaa1851d7e736f7ccb21be2525c1`. | Aprovado. |
| Calibração | `CAL-QLT-MIXTYPE-005-001`: 3 TP, 0 FP, 0 FN em seis cenários. | Aprovado para draft. |
| Privacidade | Testes impedem a emissão de conteúdo, posições, nomes de coluna e títulos de aba. | Aprovado. |

## Limites persistentes

Esta liberação não autoriza inferência de tipo de negócio, parsing de datas em texto, tratamento de sentinelas, correção automática, uso produtivo, calibração em dados reais ou promoção do Gate MVP 1.0. Os três achados positivos validam a política apenas no golden dataset agregado e não são uma taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente quando o perfil draft é selecionado. Qualquer ampliação de escopo exige novo gate humano.
