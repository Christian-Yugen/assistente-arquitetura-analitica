# QLT-WHITESPACE-009 — Política Proposta 001

**Regra:** `QLT-WHITESPACE-009 — Espaços e caracteres ocultos`.  
**Fonte de metadados:** `official-rule-blueprint-95.json`.  
**Estado:** proposta não executável, pendente de aprovação explícita de Chris.  
**Escopo oficial:** coluna.  
**Prioridade oficial:** P1.  
**Dependência oficial:** profiling.  
**Saída oficial:** finding.

## Lacuna de política reconstruída

O blueprint define o propósito de detectar sujeira textual estrutural, mas não materializa gramática, conjunto de caracteres, denominador, limiares, severidade, privacidade ou ação permitida. Esta proposta não presume que todo espaço ou caractere não imprimível seja um erro de negócio e restringe a detecção a indicadores técnicos inequívocos.

## Opção A proposta — espaços marginais e invisíveis explícitos

A regra avaliará somente textos não ausentes. Será considerado **espaço marginal** um texto não vazio que comece ou termine com espaço ASCII (`U+0020`) ou espaço não separável (`U+00A0`). Será considerado **caractere oculto explícito** a presença em qualquer posição de `U+200B`, `U+200C`, `U+200D`, `U+2060` ou `U+FEFF`.

Cada valor afetado contribuirá uma única vez ao total, mesmo que apresente mais de um sinal. Um finding será emitido somente quando existirem pelo menos três textos não ausentes e ao menos um texto afetado. A QLT-NULL-001 continua responsável por textos inteiramente vazios ou compostos somente por whitespace; tabulação, quebra de linha, controles genéricos, normalização Unicode, caixa, acentuação, pontuação, abreviações e formato semântico ficam fora deste ciclo.

| Elemento | Proposta |
|---|---|
| Denominador | Quantidade de textos não ausentes e não vazios pela semântica da QLT-NULL-001. |
| Numerador | Quantidade de textos afetados por espaço marginal e/ou caractere oculto explícito. |
| Finding | Emitir apenas com denominador mínimo de 3 e numerador maior que zero. |
| Severidade | Baixa até 5%; média acima de 5% até 20%; alta acima de 20%. |
| Evidência | Contagens agregadas de textos analisados, espaços marginais, invisíveis explícitos, textos afetados, proporção e base de normalização. |
| Pergunta | Solicitar validação humana somente em severidade média ou alta, sem identificar coluna, valor, posição ou aba. |
| Intervenção | Não limpar, substituir, aparar, normalizar, excluir ou reordenar dados. |

## Exclusões e precedência

Valores `None`, `NaN` e textos que sejam vazios após `strip()` são excluídos e permanecem sob a QLT-NULL-001. Cadeias numéricas, datas, variações categóricas e tipos mistos não são reinterpretados por esta regra; suas respectivas regras mantêm precedência. Nomes de colunas e títulos de abas não podem compor evidência, título de finding, recomendação ou pergunta.

> Esta proposta não permite implementação, alteração de planilha ou inclusão na allowlist. Qualquer ampliação para tabulações, quebras de linha, outros controles, dedução de intenção ou limpeza automática exigirá nova decisão humana.
