# REL-COMPKEY-009 — Proposta A de Política 001

## Finalidade e limite

A `REL-COMPKEY-009` trata exclusivamente de uma **hipótese de revisão** para uma chave de relacionamento composta por exatamente dois campos físicos. Ela não revela os campos, não afirma que a composição seja a chave de negócio correta, não concatena colunas e não cria relações, Power Query, DAX ou mudanças em arquivos do usuário.

> A unicidade individual insuficiente não prova a necessidade de uma chave composta. A hipótese somente surge quando a composição agregada de dois campos é a única estrutura elegível observada e exige confirmação humana.

## Proposta A — alerta conservador de chave composta

A futura regra poderá emitir somente `composite_relationship_key_review_candidate` quando um **par opaco de abas distintas** satisfizer simultaneamente as condições abaixo. A eventual avaliação de tuplas deverá ocorrer apenas de forma transitória dentro do processo do motor; os valores e suas assinaturas não podem sobreviver à agregação.

| Aspecto | Condição proposta |
|---|---|
| Classificação | A origem já foi classificada como dimensão padrão e o destino como fato transacional ou periódico. Dimensão calendário, fato sem granularidade, classificação indefinida ou conflito bloqueiam. |
| Composição | Exatamente um par de dois campos físicos elegíveis é completo e único na origem e tem referências completas e não únicas no destino. Nenhuma chave física simples elegível pode existir para o mesmo par de abas. |
| Cobertura | A cobertura referencial agregada das tuplas é exatamente `1.0`, sem referências não cobertas, e há uma única direção candidata. |
| Sinais de bloqueio | Fórmulas, sensibilidade, incompletude, cobertura parcial ou zero, autorreferência, padrões 1:1 ou N:N e ambiguidade bloqueiam. |

Se futuramente autorizada, a saída terá confiança máxima de `0.70`, severidade `review_required` e uma pergunta bloqueante equivalente a: **“A hipótese de chave composta por dois campos foi revisada e confirmada como regra de negócio? Se não, indique a chave correta ou que não deve haver relação.”** A resposta humana não pode ser inferida do workbook.

## Evidência permitida e privacidade

O futuro perfil poderá conter somente flags e métricas agregadas: compatibilidade de classificação, quantidade de pares compostos elegíveis, existência agregada de chave simples, completude, unicidade composta, cobertura referencial agregada, quantidade de direções e flags de bloqueio. Ele não poderá conter títulos de abas, cabeçalhos, valores, exemplos, posições, correspondências, frequências individuais, tuplas, chaves, identificadores, textos de célula, fórmulas ou assinaturas de valores.

`SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes: qualquer sinal de sensibilidade bloqueia a emissão. A análise e seus artefatos sintéticos devem continuar sem dados de workbooks reais.

## Exclusões explícitas

Esta proposta não autoriza classificador, profiler, perfil, registro, contrato, pipeline, catálogo executável, allowlist, teste de execução, golden dataset, calibração ou mudança na interface. A produção permanece bloqueada pelo Gate MVP 1.0.
