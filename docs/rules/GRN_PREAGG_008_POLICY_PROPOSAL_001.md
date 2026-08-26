# GRN-PREAGG-008 — Proposta A de política draft

**Regra:** `GRN-PREAGG-008 — Agregação prévia`
**Categoria:** granularidade
**Estado desta proposta:** não executável.

Uma futura implementação no perfil draft poderá somente consolidar um sinal **independente, autorizado, opaco e agregado** de que a estrutura exige revisão humana quanto a uma possível agregação prévia. O resultado permitido é uma hipótese conceitual acompanhada de pergunta humana bloqueante; ele não afirma, valida, calcula, determina ou cria agregação.

A regra não poderá inferir, identificar, calcular, somar, contar, comparar, recomputar, selecionar ou desagregar métricas, medidas, níveis de detalhe, entidades, eventos, chaves, fatos, dimensões, relações, cardinalidades, campos, valores, frequências, períodos ou conteúdo de workbook. Ela não poderá reprocessar dados privados, expor identificadores, alterar arquivos nem gerar DAX ou Power Query.

Ausência de sinal independente, confirmação humana prévia, sensibilidade, conflito estrutural, erro contratual ou lacuna de pré-condição devem suprimir qualquer finding de modo fail-closed. Perfil agregado, classificador, registro, contrato, pipeline, allowlist, testes, golden estritamente sintético, SHA-256, calibração e gate individual permanecem bloqueados até uma autorização explícita de Chris para código. **Produção permanece bloqueada.**
