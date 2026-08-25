# REL-FACTFACT-006 — Proposta A de Política 001

## Finalidade e limite

A `REL-FACTFACT-006` trata exclusivamente de uma **hipótese de revisão** sobre possível relacionamento direto entre duas abas já classificadas como fatos. A regra não confirma que o vínculo é correto, não recomenda a criação de uma relação direta, não recomenda dimensão compartilhada, tabela ponte ou direção de filtro e não altera arquivos, Power Query, DAX ou Power BI.

> A ausência de uma dimensão compartilhada observável pelo perfil draft não prova que ela não exista no modelo de negócio. A decisão de modelagem permanece humana.

## Proposta A — alerta conservador de relacionamento direto entre fatos

A futura regra poderá emitir apenas `direct_fact_to_fact_relationship_review_candidate` quando um **par opaco de abas distintas** satisfizer simultaneamente as condições abaixo. Os sinais devem ser agregados e efêmeros; identificadores opacos usados internamente para correlacionar o par não podem ser expostos, persistidos como evidência ou usados para reconstruir dados do workbook.

| Aspecto | Condição proposta |
|---|---|
| Classificação de origem e destino | As duas abas já foram classificadas como fato transacional ou fato periódico no perfil draft; fato sem granularidade, dimensão padrão, dimensão calendário ou classificação indefinida bloqueiam. |
| Estrutura física | Há exatamente uma chave física elegível, completa e única no lado de origem e exatamente uma referência física elegível, completa e não única no lado de destino. |
| Cobertura | A cobertura referencial agregada é exatamente `1.0`, sem referências não cobertas. |
| Direção | Há exatamente uma direção elegível. Autorrefêrencia e duas ou mais direções elegíveis bloqueiam. |
| Sinais de bloqueio | Fórmulas, sensibilidade, incompletude, conflito, ambiguidade, padrão 1:1 e padrão muitos-para-muitos bloqueiam. |

Se futuramente autorizada, a saída terá confiança máxima de `0.65`, severidade `review_required` e uma pergunta bloqueante equivalente a: **“A hipótese de vínculo direto entre fatos foi revisada? Confirme se existe uma dimensão compartilhada, uma relação indireta ou se não deve haver relação.”** A resposta humana não pode ser inferida do workbook.

## Evidência permitida e privacidade

O futuro perfil poderá conter somente flags e métricas agregadas: compatibilidade de classificação, contagem de chaves e referências elegíveis, completude, unicidade, cobertura referencial agregada, quantidade de direções e flags de bloqueio. Ele não poderá conter títulos de abas, cabeçalhos, valores, exemplos, posições, correspondências, frequências individuais, chaves, identificadores, textos de célula ou fórmulas.

`SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes: qualquer sinal de sensibilidade bloqueia a emissão. A análise e seus artefatos sintéticos devem continuar sem dados de workbooks reais.

## Exclusões explícitas

Esta proposta não autoriza classificador, perfil, registro, contrato, pipeline, catálogo executável, allowlist, teste de execução, golden dataset, calibração ou mudança na interface. Ela também não muda o status de produção, que permanece bloqueado pelo Gate MVP 1.0.

## Decisão solicitada

Chris deve escolher uma das alternativas abaixo antes de qualquer gate de reconstrução:

| Alternativa | Decisão |
|---|---|
| **Aprovar Proposta A** | Autoriza somente o gate de reconstrução e a preparação controlada; não autoriza implementação. |
| Ajustar a proposta | Mantém a regra bloqueada até nova política. |
| Rejeitar | Arquiva a proposta sem criar lógica executável. |
