# QLT-OUTLIER-012 — Política proposta 001

**Estado:** não executável; aguarda autorização explícita de Chris.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.  
**Fonte recuperada:** o blueprint oficial estabelece apenas a detecção de extremos estatísticos para validação, prioridade P1, escopo por coluna, dependência de profiling e saída `finding`. O Plano Mestre exige que hipóteses sejam separadas de evidências e encaminhadas para validação humana. Nenhuma condição estatística executável foi recuperada.

## Proposta A — cerca de Tukey conservadora, sem exposição de valores

Esta proposta detecta apenas observações fisicamente numéricas, finitas e predominantemente numéricas que estejam fora das cercas clássicas baseadas em intervalo interquartil: abaixo de `Q1 − 1,5 × IQR` ou acima de `Q3 + 1,5 × IQR`, em que `IQR = Q3 − Q1`. Quartis e cercas são computados transitoriamente e nunca são persistidos, serializados ou incluídos como evidência.

| Elemento | Política proposta |
|---|---|
| Elegibilidade | Coluna com pelo menos 20 números físicos finitos e participação numérica de pelo menos 80% entre as células físicas não vazias avaliadas. |
| Método | Quartis por interpolação linear sobre a sequência numérica ordenada; cerca inferior `Q1 − 1,5 × IQR` e superior `Q3 + 1,5 × IQR`. |
| Condição | Pelo menos um número físico finito estritamente abaixo da cerca inferior ou acima da cerca superior. Valores iguais às cercas não são candidatos. |
| Caso degenerado | Quando `IQR` for zero, não há finding: a regra não usa fallback por desvio padrão, z-score, MAD ou desvio absoluto. |
| Evidência | Somente contagem de números físicos, contagem de candidatos inferiores, contagem de candidatos superiores, contagem total de candidatos e proporção agregada. |
| Severidade | Baixa até 5%; média acima de 5% até 20%; alta acima de 20% dos números físicos elegíveis. |
| Confiança | Moderada: o cálculo é determinístico, mas um extremo estatístico não confirma erro de negócio. |
| Pergunta humana | Em todo finding, solicitar confirmação genérica sobre extremos legítimos, erros de digitação, mudanças de unidade, exceções operacionais ou recortes de período. |
| Intervenção | Não remover, corrigir, substituir, arredondar, winsorizar, transformar, mover ou reordenar dados. |

## Exclusões obrigatórias

A proposta exclui colunas com menos de 20 números físicos finitos, participação numérica abaixo de 80%, `IQR = 0`, números em texto, fórmulas, datas, booleanos, erros, `NaN`, infinitos, vazios e qualquer análise de identificadores, chaves, moeda, preço, saldo, percentual ou campo que exija uma regra de negócio específica. Não há comparação entre colunas, agrupamento, segmentação, tratamento de sazonalidade ou inferência semântica.

> Um finding representa uma hipótese estatística para validação humana. Ele não confirma uma anomalia de negócio nem autoriza qualquer tratamento automático.

## Evidências exigidas antes da ativação draft

Após autorização, a implementação deverá oferecer perfil imutável agregado, cálculo determinístico, testes positivos, negativos, limítrofes, de privacidade e de integração, golden dataset sem conteúdo bruto, manifesto SHA-256, relatório reprodutível de TP/FP/FN, gate individual de calibração e prova documental. A produção permanece bloqueada mesmo após uma eventual ativação draft.
