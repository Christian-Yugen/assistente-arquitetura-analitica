# QLT-NEGATIVE-011-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-NEGATIVE-011 — Valores negativos suspeitos`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-NEGATIVE-011-RECONSTRUCTION-AUTHORIZATION-001`, com a Proposta A aprovada por Chris. | Aprovado. |
| Perfil privado | `NegativeValuesProfile` mantém somente elegibilidade, contagens agregadas, razão e base técnica; não mantém cabeçalho, valores, fórmulas, posições ou títulos de aba. | Aprovado. |
| Escopo semântico fechado | A regra só admite, após normalização técnica, `quantidade`, `qtd`, `estoque`, `volume` e `idade`. | Aprovado. |
| Exclusões | Moeda, saldo, preço, valor, resultado, percentuais, fórmulas, números em texto, datas, booleanos, não finitos e bases menores que 10 são excluídos. | Aprovado. |
| Não intervenção | O avaliador não corrige, converte, exclui, preenche, arredonda, move ou reordena dados. | Aprovado. |
| Golden dataset | `GD-QLT-NEGATIVE-011-001`, agregado e sem conteúdo bruto, SHA-256 `7146db1f63b2ecf692f82981f672e8b0c80b4515bf68f2a83f005d957644981f`. | Aprovado. |
| Calibração | `CAL-QLT-NEGATIVE-011-001`: 3 TP, 0 FP, 0 FN em sete cenários, incluindo severidades, ausência de negativos, cabeçalho não elegível, base insuficiente e base técnica não autorizada. | Aprovado para draft. |
| Validação humana | Todo finding emite pergunta humana não bloqueante; a hipótese semântica não é tratada como erro confirmado. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza sinônimos, rótulos parciais, outros idiomas, inferência por distribuição, comparação entre colunas, análise de saldo, preço, resultado, moeda ou percentuais, identificação por fórmulas, números em texto, transformação automática ou uso produtivo. As métricas cobrem somente o golden dataset agregado e não representam taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Qualquer ampliação de vocabulário, sinal técnico, escopo de dados ou ambiente exige nova decisão humana, novas evidências e novo gate.
