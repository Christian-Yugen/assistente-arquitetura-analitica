# REL-BIDIR-008 — Proposta A de Política 001

## Finalidade e limite

A `REL-BIDIR-008` trata exclusivamente de uma **hipótese de revisão** para uma eventual configuração de filtro bidirecional. O MVP não importa o modelo Power BI nem suas direções de filtro existentes; portanto, esta regra não detecta nem afirma que um filtro bidirecional esteja configurado.

> O máximo que o workbook permite concluir é que uma relação candidata dimensão–fato tem uma direção lógica candidata. Ele não informa se o modelo semântico usa filtro unidirecional ou bidirecional.

## Proposta A — alerta conservador de revisão de filtro

A futura regra poderá emitir somente `bidirectional_filter_review_candidate` quando um **par opaco de abas distintas** satisfizer simultaneamente as condições abaixo. Os sinais devem ser agregados e efêmeros; identificadores opacos transitórios usados para correlacionar o par não podem ser expostos, persistidos como evidência ou usados para reconstruir dados do workbook.

| Aspecto | Condição proposta |
|---|---|
| Classificação | A origem já foi classificada como dimensão padrão e o destino como fato transacional ou periódico. Dimensão calendário, fato sem granularidade, classificação indefinida ou conflito bloqueiam. |
| Estrutura | Há exatamente uma chave física completa e única na origem, exatamente uma referência física completa e não única no destino, cobertura referencial agregada integral e uma única direção candidata. |
| Interpretação limitada | O sinal exige que qualquer configuração bidirecional futura seja revisada por humano; ele não informa a configuração existente e não recomenda ativá-la. |
| Sinais de bloqueio | Fórmulas, sensibilidade, incompletude, cobertura parcial ou zero, autorreferência, padrões 1:1 ou N:N e ambiguidade bloqueiam. |

Se futuramente autorizada, a saída terá confiança máxima de `0.70`, severidade `review_required` e uma pergunta bloqueante equivalente a: **“Se for considerada uma direção bidirecional para esta relação candidata, a exceção foi justificada e revisada? Caso contrário, preserve a direção unidirecional proposta.”** A resposta humana não pode ser inferida do workbook.

## Evidência permitida e privacidade

O futuro perfil poderá conter somente flags e métricas agregadas: compatibilidade de classificação, contagem de chaves e referências elegíveis, completude, unicidade, cobertura referencial agregada, quantidade de direções e flags de bloqueio. Ele não poderá conter títulos de abas, cabeçalhos, valores, exemplos, posições, correspondências, frequências individuais, chaves, identificadores, textos de célula ou fórmulas.

`SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes: qualquer sinal de sensibilidade bloqueia a emissão. A análise e seus artefatos sintéticos devem continuar sem dados de workbooks reais.

## Exclusões explícitas

Esta proposta não autoriza classificador, perfil, registro, contrato, pipeline, catálogo executável, allowlist, teste de execução, golden dataset, calibração ou mudança na interface. Ela não acessa um modelo Power BI nem cria ou modifica relações, filtros, Power Query, DAX ou arquivos de usuário. A produção permanece bloqueada pelo Gate MVP 1.0.
