# QLT-NEGATIVE-011-RECONSTRUCTION-AUTHORIZATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Decisor:** Chris.  
**Decisão:** **Aprovada a Proposta A para implementação exclusiva no perfil draft.**  
**Produção:** bloqueada.

## Objeto da autorização

Este gate autoriza a implementação da `QLT-NEGATIVE-011 — Valores negativos suspeitos` somente conforme `QLT_NEGATIVE_011_POLICY_PROPOSAL_001.md` e `QLT_NEGATIVE_011_LOGICAL_SPEC_PROPOSAL_001.md`. A fonte oficial a classifica como P1, com escopo por coluna, dependente de profiling e saída `finding`; a condição determinística foi reconstruída por ausência de uma especificação materializada.

| Elemento | Decisão aprovada |
|---|---|
| Vocabulário fechado | Cabeçalho normalizado pertence exatamente a `quantidade`, `qtd`, `estoque`, `volume` ou `idade`. |
| Base mínima | Pelo menos 10 números físicos, finitos e não booleanos. |
| Sinal | Pelo menos um número físico estritamente menor que zero. |
| Evidência | Contagem de números físicos, contagem de negativos, proporção, elegibilidade e base técnica; sem cabeçalho, valores, fórmulas, posições ou títulos de aba. |
| Severidade | Baixa até 5%; média acima de 5% até 20%; alta acima de 20%. |
| Confiança e pergunta | Confiança moderada e pergunta humana genérica em toda ocorrência. |
| Intervenção | Não converter, corrigir, excluir, preencher, arredondar, mover ou reordenar dados. |

## Exclusões mandatórias

Não estão autorizadas inferência de domínio fora do vocabulário fechado, números em texto, fórmulas, datas, booleanos, erros, números não finitos, bases com menos de 10 números físicos, saldo, valor, preço, resultado, percentuais, moeda, contas contábeis, regras de soma, comparação entre colunas, detecção de outliers ou transformações automáticas.

## Evidências obrigatórias antes da allowlist

A implementação deverá produzir perfil privado agregado, testes positivos, negativos, limítrofes, de privacidade e integração, golden dataset sem conteúdo bruto, manifesto SHA-256, avaliador de calibração reprodutível, relatório TP/FP/FN, gate individual de calibração e prova documental. A entrada na allowlist depende da aprovação expressa desses controles.

> A autorização de Chris permite somente este ciclo draft. Não libera produção, não amplia o vocabulário e não substitui o gate de calibração nem o Gate MVP 1.0.
