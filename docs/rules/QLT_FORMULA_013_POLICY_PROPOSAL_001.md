# QLT-FORMULA-013 — Política proposta 001

**Estado:** não executável; aguarda autorização explícita de Chris.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.  
**Fonte recuperada:** o blueprint oficial estabelece somente a detecção de padrões de fórmula divergentes, prioridade P1, escopo por coluna, dependência de profiling e saída `finding`. O Plano Mestre exige evidência controlada e validação humana. Nenhuma condição ou política de privacidade executável foi recuperada.

## Proposta A — interrupção de padrão fórmula versus valor, sem ler expressões

Esta proposta deliberadamente não compara o conteúdo de fórmulas. Ela detecta apenas a presença de uma ou mais células físicas não vazias **sem fórmula** em uma coluna predominantemente composta por células identificadas pelo tipo interno `f` do XLSX. A regra classificará transitoriamente apenas o tipo da célula; não armazenará, analisará, normalizará ou emitirá a expressão da fórmula, seus valores calculados ou suas referências.

| Elemento | Política proposta |
|---|---|
| Elegibilidade | Pelo menos 10 células físicas não vazias, ao menos 8 células do tipo fórmula e participação de fórmulas de pelo menos 80%. |
| Condição | Pelo menos uma célula física não vazia que não seja fórmula na coluna elegível. Células vazias não contam como ruptura. |
| Evidência | Contagem de células físicas não vazias, contagem de fórmulas, contagem de não fórmulas e proporção agregada de não fórmulas; sem expressão, referência, valor, cabeçalho, posição ou título de aba. |
| Severidade | Baixa até 5%; média acima de 5% até 10%; alta acima de 10% de não fórmulas entre células físicas não vazias. |
| Confiança | Moderada: a classificação do tipo é determinística, mas uma substituição manual pode ser intencional e não representa, por si, erro. |
| Pergunta humana | Em todo finding, perguntar genericamente se as substituições manuais foram intencionais ou se a coluna deveria manter cálculo consistente. |
| Intervenção | Não criar, copiar, corrigir, preencher, apagar, recalcular, mover ou reordenar fórmulas ou valores. |

## Exclusões obrigatórias

A proposta exclui colunas com menos de 10 células físicas não vazias, menos de 8 fórmulas ou participação de fórmulas inferior a 80%. Exclui células vazias, fórmulas ausentes em linhas inteiramente vazias, conteúdo de expressões, referências de célula, valores calculados, fórmulas com ou sem erro, fórmulas de matriz, diferença entre duas fórmulas, padrões de referência relativa, comparação de abas e avaliação do significado de qualquer valor manual.

> Um finding identifica uma ruptura material de presença versus ausência de fórmula. Ele não conclui que a fórmula deveria existir, que o valor manual está incorreto ou que qualquer fórmula deve ser copiada automaticamente.

## Evidências exigidas antes da ativação draft

Após autorização, a implementação deverá usar leitura não invasiva de tipos de células (`data_type`) e um perfil imutável agregado. Deverá incluir testes positivos, negativos, limítrofes, de privacidade e de integração, golden dataset sem expressões ou dados brutos, manifesto SHA-256, relatório reprodutível de TP/FP/FN, gate individual de calibração e prova documental. A produção permanece bloqueada mesmo após uma eventual ativação draft.
