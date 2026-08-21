# QLT-WHITESPACE-009-RECONSTRUCTION-AUTHORIZATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Decisor:** Chris.  
**Decisão:** **Aprovada a Opção A para implementação exclusiva no perfil draft.**  
**Produção:** bloqueada.

## Objeto da autorização

Este gate autoriza a implementação da `QLT-WHITESPACE-009 — Espaços e caracteres ocultos` somente conforme `QLT_WHITESPACE_009_POLICY_PROPOSAL_001.md` e `QLT_WHITESPACE_009_LOGICAL_SPEC_PROPOSAL_001.md`. O blueprint oficial classifica a regra como P1, de escopo por coluna, dependente de profiling e com saída `finding`.

## Escopo aprovado

| Elemento | Decisão aprovada |
|---|---|
| Espaço marginal | Texto não vazio que comece ou termine com `U+0020` ou `U+00A0`. |
| Invisível explícito | Presença de `U+200B`, `U+200C`, `U+200D`, `U+2060` ou `U+FEFF` em qualquer posição. |
| Condição | Ao menos três textos não ausentes e ao menos um texto afetado. |
| Evidência | Somente contagens, proporção e base de normalização; sem valores, exemplos, posições, nomes de coluna ou abas. |
| Severidade | Baixa até 5%; média acima de 5% até 20%; alta acima de 20%. |
| Pergunta | Apenas para severidade média ou alta, sem identificar a coluna. |
| Intervenção | Não limpar, substituir, aparar, normalizar, excluir ou reordenar dados. |

## Exclusões mandatórias

Textos vazios ou formados apenas por whitespace permanecem sob a QLT-NULL-001. Não estão autorizados tabulações, quebras de linha, controles genéricos, normalização Unicode, análise de caixa, acentuação, pontuação, inferência de intenção ou limpeza automática. Regras de números em texto, variações categóricas e tipos mistos continuam responsáveis por seus próprios escopos.

## Evidências obrigatórias antes da allowlist

A implementação deverá produzir perfil agregado, testes unitários positivos, negativos, limítrofes e de privacidade, golden dataset sem conteúdo bruto, manifesto SHA-256, avaliador de calibração reprodutível, gate individual de calibração e prova documental. A entrada na allowlist depende de métricas explícitas de TP, FP e FN no dataset autorizado.

> A autorização de Chris permite somente este ciclo draft. Não libera produção, não amplia o conjunto de caracteres e não substitui o gate de calibração nem o Gate MVP 1.0.
