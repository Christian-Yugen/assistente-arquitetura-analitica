# Proposta A — REL-BRIDGE-005: Necessidade de ponte

**Estado:** ativada somente em draft. **Regra oficial:** `REL-BRIDGE-005`, categoria `relationship`, prioridade `P1`, escopo `sheet_pair`, etapa `relationship_inference`, dependência declarada `table_classification` e saída primária `relationship_or_finding`.

## Finalidade limitada

Esta proposta define somente os limites de uma futura implementação draft. Caso Chris autorize código explicitamente em um ciclo posterior, a regra poderá consolidar um sinal **independente, autorizado, opaco e agregado** de necessidade de revisão humana sobre uma possível necessidade de ponte. O único resultado admissível seria uma pergunta humana bloqueante; não haverá decisão automática.

## Exclusões obrigatórias

A regra não poderá detectar, recomendar, classificar, propor, confirmar ou criar tabela ponte, ponte, relacionamento, dimensão, fato, entidade, tabela, chave, atributo, relação, cardinalidade, granularidade, período, métrica, campo, valor, frequência, pares ou conteúdo de workbook. Ela não poderá escolher campos, indicar fontes, gerar DAX ou Power Query, calcular métricas nem revelar dados privados, posições, cabeçalhos, títulos ou amostras.

## Guardas e evidência

Qualquer desenho futuro deverá receber exclusivamente contagens e flags agregadas de uma fonte independente autorizada. A ausência desse sinal, confirmação humana, sensibilidade, conflito, erro contratual ou falta de gate deverá produzir zero candidatos, de modo **fail-closed**. O pipeline real deverá fixar o sinal independente em zero até que exista fonte autorizada; dados do workbook nunca poderão gerar ou alimentar esse sinal.

## Critérios para eventual código draft

Chris autorizou explicitamente o código draft em `Chat: SIM, autorizado`. O perfil agregado, classificador determinístico, integração em registro e contrato, pipeline com sinal zero, allowlist, testes, golden exclusivamente sintético com SHA-256, calibração limitada com TP/FP/FN e gate individual foram vinculados a essa autorização. **Produção permanece bloqueada.**
