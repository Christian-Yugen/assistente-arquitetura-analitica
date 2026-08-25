# MET-WAVG-011 — Proposta A de Política 001

A futura `MET-WAVG-011` poderá sugerir somente uma **média ponderada conceitual, revisável e não calculada** quando houver granularidade única definida, sinais agregados de exatamente um par compatível de medida e peso, e confirmação agregada de pesos estritamente positivos. A fórmula possível será somente `weighted_sum(eligible_measure, eligible_weight) / total(eligible_weight)`; a regra não selecionará campos, não atribuirá papéis, não definirá unidade, população, período, filtros, tratamento de pesos, arredondamento ou partições, não calculará resultado, não exporá valores e não gerará DAX/M.

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade, peso ausente, não positivo ou múltiplos pares candidatos bloquearão uma futura emissão. A saída terá, no máximo, confiança `0.60`, evidência exclusivamente agregada e pergunta humana bloqueante para confirmar medida, peso, unidade, população, período, filtros, tratamento de peso e arredondamento.

> Esta Proposta A é estritamente não executável. Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção.
