# Gate de Calibração Draft — MDL-FACTNOGRAIN-019

**Status:** aprovado exclusivamente para o perfil draft controlado.

O gate registra a calibração `CAL-MDL-FACTNOGRAIN-019-001` contra o dataset exclusivamente sintético `GD-MDL-FACTNOGRAIN-019-001`, registrado no manifesto `MANIFEST-GD-MDL-FACTNOGRAIN-019-001` e assinado com SHA-256 `3466965e28f9c0227dded94e8d9277667cce7939db778c4c8b255684c9be62fc`. O avaliador reproduzível `engine.calibration.evaluate_mdl_factnograin_draft_golden.evaluate` reporta **3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos**.

A regra somente emite `fact_without_defined_grain_candidate` quando há ao menos vinte linhas observadas, uma ou mais medidas numéricas físicas elegíveis, sinal agregado de fato e nenhuma hipótese de granularidade ativa. Fórmulas, sensibilidade, candidato dimensional, temporalidade incompatível ou ambiguidade bloqueiam integralmente a saída.

O perfil, a evidência e o dataset retêm apenas contagens e booleanos agregados. Eles não retêm ou expõem cabeçalhos, valores, posições, frequências individuais, exemplos ou títulos de abas. O mascaramento independente e a `SEM-SENS-015` permanecem controles obrigatórios.

Esta ativação decorre da Proposta A aprovada por Chris, do `MDL-FACTNOGRAIN-019-RECONSTRUCTION-AUTHORIZATION-001` e da autorização explícita posterior para implementação draft. A pergunta humana continua bloqueante e a produção permanece bloqueada: a classificação não confirma uma tabela fato nem define granularidade, relacionamentos, medidas ou recomendações produtivas.
