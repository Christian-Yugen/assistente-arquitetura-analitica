# REL-CONFORMED-010 — Proposta A de Política 001

## Finalidade e limite

A `REL-CONFORMED-010` trata exclusivamente de uma **hipótese de revisão** de que uma dimensão candidata pode estar conectada a dois ou mais fatos por relações unidirecionais igualmente elegíveis. A regra não confirma conformidade de negócio, não conhece o significado dos campos e não cria dimensão compartilhada, relações, filtros, Power Query, DAX ou alterações em arquivos.

> Duas conexões físicas completas não provam que a dimensão seja conformada. A semântica compartilhada, os papéis da dimensão e a regra de negócio exigem confirmação humana.

## Proposta A — alerta conservador de dimensão compartilhada

A futura regra poderá emitir somente `conformed_dimension_review_candidate` para um **par opaco dimensão–fato** quando a dimensão de origem também tiver pelo menos uma conexão candidata independente com outro fato, sem revelar qual é esse outro fato. Todos os sinais devem ser agregados e efêmeros.

| Aspecto | Condição proposta |
|---|---|
| Classificação | A origem já foi classificada como dimensão padrão e o destino como fato transacional ou periódico. Dimensão calendário, fato sem granularidade, classificação indefinida ou conflito bloqueiam. |
| Conexão do par | Exatamente uma chave completa e única na dimensão, uma referência completa e não única no fato, cobertura referencial agregada de `1.0` e uma direção candidata. |
| Compartilhamento agregado | A mesma dimensão tem `2` ou mais fatos candidatos conectados por sinais igualmente completos, sem expor ou enumerar os fatos. |
| Sinais de bloqueio | Fórmulas, sensibilidade, incompletude, cobertura parcial ou zero, autorreferência, padrões 1:1 ou N:N e ambiguidade bloqueiam. |

Se futuramente autorizada, a saída terá confiança máxima de `0.75`, severidade `review_required` e uma pergunta bloqueante equivalente a: **“A dimensão candidata foi revisada como dimensão compartilhada entre fatos? Confirme o significado comum e as conexões autorizadas antes de orientar a modelagem.”** A resposta humana não pode ser inferida do workbook.

## Evidência permitida e privacidade

O futuro perfil poderá conter somente flags e métricas agregadas: compatibilidade de classificação, elegibilidade do par, cobertura, direção e `connected_fact_count`. Ele não poderá conter títulos de abas, cabeçalhos, valores, exemplos, posições, correspondências, frequências individuais, chaves, identificadores ou a lista de fatos conectados.

`SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes: qualquer sinal de sensibilidade bloqueia a emissão. A análise e os artefatos sintéticos devem continuar sem dados de workbooks reais.

## Exclusões explícitas

Esta proposta não autoriza classificador, perfil, registro, contrato, pipeline, catálogo executável, allowlist, teste de execução, golden dataset, calibração ou mudança na interface. Ela não cria dimensão conformada, não substitui dimensões existentes e não altera relacionamentos ou filtros. A produção permanece bloqueada pelo Gate MVP 1.0.
