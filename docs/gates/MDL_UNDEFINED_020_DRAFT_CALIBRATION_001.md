# Gate de Calibração Draft — MDL-UNDEFINED-020

**Status:** aprovado exclusivamente para o perfil draft controlado.

O gate registra a calibração `CAL-MDL-UNDEFINED-020-001` contra o dataset exclusivamente sintético `GD-MDL-UNDEFINED-020-001`, registrado no manifesto `MANIFEST-GD-MDL-UNDEFINED-020-001` e assinado com SHA-256 `f3c70027a3bdc9b4a2f83255239118b5e0566fe3c7bf9bc140d80a779c2571a1`. O avaliador reproduzível `engine.calibration.evaluate_mdl_undefined_draft_golden.evaluate` reporta **3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos**.

A regra somente emite `table_classification_undefined_candidate` quando há ao menos vinte linhas observadas, duas ou mais colunas físicas e a avaliação completa dos cinco classificadores fechados de tabela não produz candidato positivo, conflito, fórmula, sensibilidade ou ambiguidade. Esse marcador é residual: ele não prova que a aba seja fato, dimensão, erro, irrelevante ou semanticamente desconhecida.

O perfil, a evidência e o dataset retêm apenas contagens e booleanos agregados. Eles não retêm ou expõem cabeçalhos, valores, posições, frequências individuais, exemplos, títulos de abas ou identidades dos classificadores individuais. O mascaramento independente e a `SEM-SENS-015` permanecem controles obrigatórios.

Esta ativação decorre da Proposta A aprovada por Chris, do `MDL-UNDEFINED-020-RECONSTRUCTION-AUTHORIZATION-001` e da autorização explícita posterior para implementação draft. A pergunta humana continua bloqueante e a produção permanece bloqueada: o marcador exige a confirmação da finalidade analítica e do grão antes de qualquer modelagem.
