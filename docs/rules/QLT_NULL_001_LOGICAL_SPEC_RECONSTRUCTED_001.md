# QLT-NULL-001 — Especificação Lógica Reconstruída

**Versão candidata:** `0.1.0-reconstructed.1`.  
**Status:** rascunho para revisão de governança; **não executável**.

O avaliador receberá somente um `NullColumnProfile` agregado. O perfil não pode carregar valores brutos, título de aba original, amostras de sentinelas ou resultados de fórmulas. Essa limitação mantém o diagnóstico explicável e compatível com a política de minimização de dados do MVP draft.

| Métrica agregada | Definição |
|---|---|
| `observed_cell_count` | Número de células para a coluna em linhas de dados incluídas. |
| `non_missing_cell_count` | Número de células não classificadas como ausentes. |
| `structural_null_count` | Células lidas como `None`. |
| `blank_text_count` | Textos cujo conteúdo, após `strip`, é vazio. |
| `numeric_nan_count` | Valores numéricos `NaN`. |
| `missing_cell_count` | Soma das três classes determinísticas de ausência. |
| `missing_ratio` | `missing_cell_count / observed_cell_count`. |

Uma linha de dados só participa quando alguma célula limitada aos cabeçalhos contém conteúdo não ausente ou uma expressão de fórmula. Linhas inteiramente vazias e linhas de formatação não ampliam o denominador. Uma coluna sem célula observada, sem célula não ausente ou sem ausência é excluída da regra; o caso integralmente vazio pertence a diagnóstico próprio.

| Razão calculada | Resultado | Pergunta |
|---|---|---|
| Maior que 0% e menor que 5% | Finding de severidade baixa. | Não aplicável. |
| De 5% a menor que 20% | Finding de severidade média. | Não aplicável. |
| Igual ou superior a 20%, com 20 ou mais células observadas | Finding de severidade alta. | Pergunta bloqueante sobre o significado de negócio da ausência. |
| Igual ou superior a 20%, com menos de 20 células observadas | Finding de severidade alta com confiança 0,60. | Não aplicável; a amostra não permite pergunta bloqueante. |

A confiança inicia em 0,90 para amostras com pelo menos 20 células observadas e em 0,60 abaixo desse limite. Quando mais de uma classe determinística de ausência ocorre, aplica-se penalidade de 0,10, limitada a 0,50. As evidências são exclusivamente as contagens, proporção e distribuição entre classes.

> A matriz de testes deverá cobrir casos de fronteira de 5% e 20%, ausência estrutural, branco textual, `NaN`, amostra pequena, mistura de classes, coluna integralmente vazia, sentinelas textuais e fórmulas. Nenhuma implementação será iniciada antes da aprovação explícita do gate de reconstrução.
