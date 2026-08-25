# MET-RUNNING-010 — Proposta A de Política 001

A futura `MET-RUNNING-010` poderá sugerir somente um **acumulado conceitual, revisável e não calculado** quando houver granularidade temporal única definida, sinais agregados de exatamente uma medida elegível e uma ordenação temporal elegível sem ambiguidade. A fórmula possível será somente `cumulative eligible_measure ordered by eligible_time`; a regra não selecionará campos, não definirá ordem, unidade, população, período, partição, filtros, reinício ou arredondamento, não calculará resultado, não exporá valores e não gerará DAX/M.

Sensibilidade, fórmulas, classificação/grão temporais indefinidos, fato sem grão, conflito, ambiguidade de ordenação, ausência de medida/tempo ou múltiplas combinações candidatas bloquearão uma futura emissão. A saída terá, no máximo, confiança `0.60`, evidência exclusivamente agregada e pergunta humana bloqueante para confirmar medida, ordem temporal, partição, população, período, filtros e ponto de reinício.

> Esta Proposta A é estritamente não executável. Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção.
