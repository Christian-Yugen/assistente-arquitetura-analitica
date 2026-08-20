# QLT-BADDATE-006 — Política Proposta 001

**Estado:** proposta não executável; requer aprovação explícita de Chris.  
**Regra oficial:** `QLT-BADDATE-006 — Datas inválidas`.  
**Fonte de metadados:** `artifacts/catalogs/official-rule-blueprint-95.json`.  
**Prioridade e escopo:** P0, por coluna, dependente de profiling.  
**Propósito oficial:** detectar valores que não podem ser convertidos em datas.

## Lacuna de origem e decisão de reconstrução

O blueprint oficial informa apenas identificador, título, propósito, prioridade, escopo, dependência e saída primária. Ele não materializa gramática de datas, locale, limiares, severidade, evidência ou exclusões. Esta política propõe uma reconstrução limitada para evitar que uma regra de qualidade transforme formatos regionais, códigos ou números em alegações de data inválida.

## Opção A revisada — ISO e brasileiro estritos sem inferência ampla

Avaliar apenas textos não ausentes que tenham exatamente o formato `AAAA-MM-DD`, `DD-MM-AAAA` ou `DD/MM/AAAA`, conforme as expressões `^\d{4}-\d{2}-\d{2}$`, `^\d{2}-\d{2}-\d{4}$` e `^\d{2}/\d{2}/\d{4}$`. O primeiro será validado pelo parser determinístico `date.fromisoformat`; os formatos brasileiros, por `datetime.strptime(valor, "%d-%m-%Y")` e `datetime.strptime(valor, "%d/%m/%Y")`. Um valor elegível que não puder ser convertido pelo parser correspondente será contado como candidato inválido.

| Aspecto | Política proposta |
|---|---|
| Gatilho | Emitir finding quando houver ao menos um texto em formato ISO ou brasileiro estrito que não seja uma data de calendário válida. |
| Denominador | Quantidade de textos nos formatos estritos `AAAA-MM-DD`, `DD-MM-AAAA` ou `DD/MM/AAAA`, válidos ou inválidos. |
| Severidade | Baixa até 5% de inválidos, média acima de 5% até 20%, alta acima de 20%. |
| Evidência permitida | Contagem de candidatos ISO, contagem inválida, proporção inválida e identificador da base de normalização. |
| Pergunta humana | Apenas para severidade média ou alta, sem identificar coluna, aba, posição ou valor. |
| Intervenção | Nenhuma conversão, correção, remoção, preenchimento ou reordenação de célula. |

## Exclusões obrigatórias

Ficam fora da regra os valores ausentes, células `date` ou `datetime` nativas, serial numérico do Excel, mês por extenso, horários, fusos, fórmulas, códigos, formatos com barra que não sejam `DD/MM/AAAA` e qualquer formato que não corresponda exatamente a `AAAA-MM-DD`, `DD-MM-AAAA` ou `DD/MM/AAAA`. Textos numéricos continuam pertencendo à QLT-NUMTEXT-007; tipos mistos continuam pertencendo à QLT-MIXTYPE-005.

> A Opção A não afirma que formatos excluídos são válidos ou inválidos. Ela registra apenas a ausência deliberada de inferência semântica ou regional no perfil draft.

## Condições para implementação e ativação

Se aprovada, a implementação deverá produzir somente perfil agregado, testes positivos, negativos, limítrofes e de privacidade, golden dataset sem conteúdo bruto, manifesto SHA-256, avaliador de calibração reprodutível e gate individual. A regra permanecerá fora da allowlist até a aprovação desse gate e não poderá liberar produção.
