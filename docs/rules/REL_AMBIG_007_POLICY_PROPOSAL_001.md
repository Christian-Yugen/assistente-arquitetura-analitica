# REL-AMBIG-007 — Proposta A de Política 001

## Finalidade e limite

A `REL-AMBIG-007` trata exclusivamente de uma **hipótese de revisão** sobre mais de uma direção de relacionamento candidata entre o mesmo par opaco de abas. Ela não detecta caminhos existentes em um modelo Power BI, pois o MVP não importa um modelo semântico nem a configuração de filtros já criada pelo usuário.

> Esta regra não demonstra que exista ambiguidade no Power BI. Ela apenas informa que os sinais agregados do workbook não permitem escolher uma única direção candidata com segurança.

## Proposta A — alerta conservador de direções candidatas concorrentes

A futura regra poderá emitir somente `ambiguous_relationship_path_review_candidate` quando um **par opaco de abas distintas** satisfizer simultaneamente as condições abaixo. Os sinais devem ser agregados e efêmeros; identificadores opacos transitórios usados para correlacionar o par não podem ser expostos, persistidos como evidência ou usados para reconstruir dados do workbook.

| Aspecto | Condição proposta |
|---|---|
| Classificação | A origem já foi classificada como dimensão padrão e o destino como fato transacional ou periódico. Dimensão calendário, fato sem granularidade, classificação indefinida ou conflito bloqueiam. |
| Estrutura | Há uma ou mais chaves físicas completas e únicas na origem, uma ou mais referências físicas completas e não únicas no destino e cobertura referencial agregada integral em cada direção contada. |
| Ambiguidade candidata | Há duas ou mais direções candidatas elegíveis agregadas para o mesmo par, sem identificar quais colunas as formam. |
| Sinais de bloqueio | Fórmulas, sensibilidade, incompletude, cobertura parcial ou zero, autorreferência, padrões 1:1 ou N:N e inconsistência de classificação bloqueiam. |

Se futuramente autorizada, a saída terá confiança máxima de `0.60`, severidade `review_required` e uma pergunta bloqueante equivalente a: **“As direções candidatas concorrentes foram revisadas antes de orientar a modelagem? Confirme a única direção válida ou indique que não deve haver relação.”** A resposta humana não pode ser inferida do workbook.

## Evidência permitida e privacidade

O futuro perfil poderá conter somente flags e métricas agregadas: compatibilidade de classificação, contagem de chaves e referências elegíveis, completude, unicidade, cobertura referencial agregada, quantidade de direções e flags de bloqueio. Ele não poderá conter títulos de abas, cabeçalhos, valores, exemplos, posições, correspondências, frequências individuais, chaves, identificadores, textos de célula ou fórmulas.

`SEM-SENS-015`, mascaramento e `sensitivity_classifications` são controles independentes: qualquer sinal de sensibilidade bloqueia a emissão. A análise e seus artefatos sintéticos devem continuar sem dados de workbooks reais.

## Exclusões explícitas

Esta proposta não autoriza classificador, perfil, registro, contrato, pipeline, catálogo executável, allowlist, teste de execução, golden dataset, calibração ou mudança na interface. Ela não inspeciona relações, direções de filtro ou caminhos de modelos Power BI existentes e não cria ou modifica relações, filtros, Power Query, DAX ou arquivos de usuário. A produção permanece bloqueada pelo Gate MVP 1.0.

## Decisão solicitada

Chris deve escolher uma das alternativas abaixo antes de qualquer gate de reconstrução:

| Alternativa | Decisão |
|---|---|
| **Aprovar Proposta A** | Autoriza somente o gate de reconstrução e a preparação controlada; não autoriza implementação. |
| Ajustar a proposta | Mantém a regra bloqueada até nova política. |
| Rejeitar | Arquiva a proposta sem criar lógica executável. |
