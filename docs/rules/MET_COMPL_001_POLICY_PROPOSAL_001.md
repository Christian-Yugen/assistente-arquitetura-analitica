# MET-COMPL-001 — Proposta A de Política 001

## Finalidade e limite

A `MET-COMPL-001` trata exclusivamente de uma **recomendação conceitual revisável** para percentual de conclusão. Ela pode indicar que uma aba com grão definido e um candidato de status parece ter estrutura adequada para discussão de uma métrica, mas não calcula percentual, não interpreta valores de status e não produz DAX, Power Query ou alteração de modelo.

> A identificação de uma coluna candidata de status não define quais estados são concluídos, cancelados, em andamento ou elegíveis para o denominador. Essas escolhas são regras de negócio e exigem confirmação humana.

## Proposta A — recomendação conceitual conservadora

A futura regra poderá emitir somente `completion_rate_conceptual_metric_candidate` para uma **aba opaca** quando satisfizer simultaneamente as condições abaixo. Todos os sinais devem ser agregados; nenhum valor de status, cabeçalho, posição ou identificador pode ser incluído no perfil ou na saída.

| Aspecto | Condição proposta |
|---|---|
| Cobertura mínima | A aba possui ao menos 20 linhas e duas ou mais colunas físicas avaliáveis. |
| Dependências | Há exatamente um candidato semântico de status e uma hipótese única de granularidade definida (evento, entidade ou chave explícita) no perfil draft. |
| Elegibilidade | Não há sensibilidade, fórmula nos sinais usados, classificação indefinida, conflito, ambiguidade ou fato sem grão. |
| Saída | A regra propõe apenas a fórmula conceitual `itens concluídos / itens elegíveis`, sem escolher estados ou calcular resultado. |

Se futuramente autorizada, a saída terá confiança máxima de `0.60`, severidade `review_required` e uma pergunta bloqueante equivalente a: **“Quais estados contam como concluídos e quais devem entrar no denominador da métrica de conclusão?”** A resposta humana não pode ser inferida do workbook.

## Evidência permitida e privacidade

O futuro perfil poderá conter somente contagens e flags agregadas: quantidade de linhas/colunas, quantidade de candidatos de status, presença de grão definido, contagem de conflitos e flags de fórmula/sensibilidade. Ele não poderá conter valores de status, cabeçalhos, títulos, exemplos, posições, correspondências, frequências individuais, identificadores, textos de célula ou fórmulas.

`SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes: qualquer sinal de sensibilidade bloqueia a emissão. A análise e os artefatos sintéticos devem continuar sem dados de workbooks reais.

## Exclusões explícitas

Esta proposta não autoriza classificador, perfil, registro, contrato, pipeline, catálogo executável, allowlist, teste de execução, golden dataset, calibração ou mudança na interface. Ela não calcula percentual, não determina numerator/denominador, não gera DAX/M e não altera arquivos ou modelos Power BI. A produção permanece bloqueada pelo Gate MVP 1.0.
