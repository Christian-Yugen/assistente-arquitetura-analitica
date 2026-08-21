# QLT-TOTALROW-010-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-TOTALROW-010 — Linhas totalizadoras`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-TOTALROW-010-RECONSTRUCTION-AUTHORIZATION-001`, com a Opção A aprovada por Chris. | Aprovado. |
| Perfil privado | `TotalRowsProfile` mantém apenas contagens agregadas, proporção e base de normalização; não retém rótulos, valores, fórmulas, posições nem títulos de aba. | Aprovado. |
| Sinais limitados | A detecção requer três linhas não vazias anteriores, primeiro rótulo significativo normalizado por NFKC e `casefold` igual a `total`, `subtotal` ou `total geral`, além de número físico complementar na linha. | Aprovado. |
| Severidade e validação | A severidade é determinada pela proporção agregada de candidatos; perguntas humanas são emitidas somente para severidade média ou alta. | Aprovado. |
| Não intervenção | O avaliador não altera, exclui, cria, move ou reordena células, linhas, fórmulas, abas ou arquivos. | Aprovado. |
| Golden dataset | `GD-QLT-TOTALROW-010-001`, agregado e sem dados brutos, SHA-256 `2a4386f9bec7af12b0ab6a69499aedb95831979e643191aac5aa68ac2118697b`. | Aprovado. |
| Calibração | `CAL-QLT-TOTALROW-010-001`: 3 TP, 0 FP, 0 FN em seis cenários, incluindo baixa, média e alta incidência, ausência de candidatos, prefixo insuficiente e base não autorizada. | Aprovado para draft. |
| Privacidade | Testes impedem a serialização de valores brutos, posições, números de linha, exemplos sensíveis e títulos de aba. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza sinônimos, traduções, rótulos parciais, identificação por fórmulas, números armazenados em texto, candidatos anteriores à terceira linha não vazia, limpeza ou separação automática de linhas, uso produtivo ou calibração em dados reais. As métricas cobrem somente o golden dataset agregado e não representam uma taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Qualquer ampliação de vocabulário, sinal técnico, escopo de dados ou ambiente exige nova decisão humana, novo conjunto de evidências e novo gate.
