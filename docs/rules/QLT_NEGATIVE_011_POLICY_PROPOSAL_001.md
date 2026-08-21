# QLT-NEGATIVE-011 — Política proposta 001

**Estado:** não executável; aguarda autorização explícita de Chris.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.  
**Fonte recuperada:** o blueprint oficial estabelece somente que a regra é P1, depende de profiling, possui escopo por coluna e emite `finding`; o Plano Mestre confirma o princípio de separar evidência de hipótese e exigir validação humana para ambiguidades. Não foi recuperada uma especificação materializada da regra.

## Proposta A — sinal físico em vocabulário fechado de semântica não negativa

Esta proposta não presume que todo número negativo é um erro. Ela produz um finding apenas quando um **valor numérico físico negativo** ocorre em uma coluna cujo cabeçalho, usado transitóriamente e nunca serializado, corresponde exatamente a um vocabulário português fechado de medidas normalmente não negativas: `quantidade`, `qtd`, `estoque`, `volume` ou `idade`.

| Elemento | Política proposta |
|---|---|
| Elegibilidade da coluna | Cabeçalho normalizado por NFKC, `casefold`, remoção de acentos, espaços extremos e internos colapsados igual a um dos cinco termos autorizados. |
| Base numérica | Pelo menos 10 valores numéricos físicos finitos, excluídos booleanos, datas, erros, vazios, `NaN`, infinitos, fórmulas e números em texto. |
| Condição | Pelo menos um número físico estritamente menor que zero entre os valores elegíveis. Zeros não contam como negativos. |
| Evidência | Apenas contagem de números físicos elegíveis, contagem de negativos e proporção agregada; sem valores, cabeçalho, posições, amostras, fórmulas ou título de aba. |
| Severidade | Baixa até 5%; média acima de 5% até 20%; alta acima de 20%. |
| Confiança | Moderada: a observação do sinal físico é determinística, mas a incompatibilidade semântica continua uma hipótese. |
| Pergunta humana | Emitir uma pergunta genérica em qualquer finding para confirmar se negativos no campo potencialmente não negativo representam ajuste, estorno, codificação ou erro de origem. |
| Intervenção | Não converter, corrigir, excluir, arredondar, substituir, preencher, mover ou reordenar dados. |

## Exclusões obrigatórias

A proposta exclui toda coluna cujo cabeçalho não corresponda exatamente ao vocabulário fechado; portanto, não avalia `valor`, `preço`, `saldo`, `resultado`, `variação`, `lucro`, moeda, percentuais, medidas de balanço, contas contábeis ou campos em outros idiomas. Também exclui colunas com menos de 10 números físicos elegíveis, números em texto, fórmulas, datas, booleanos, valores não finitos e qualquer inferência por distribuição, soma, média, outlier, tipo semântico ou regra de negócio.

> Um finding desta regra é um **sinal para validação humana**, não uma conclusão de erro e não uma autorização de transformação automática.

## Evidências exigidas antes da ativação draft

Após autorização, a implementação deverá fornecer um perfil imutável e agregado, avaliador determinístico, testes positivos, negativos, limítrofes, de privacidade e de integração, golden dataset sem conteúdo bruto, manifesto SHA-256, relatório reprodutível de TP/FP/FN, gate individual de calibração e prova documental. A produção permanece bloqueada mesmo após uma eventual ativação draft.
