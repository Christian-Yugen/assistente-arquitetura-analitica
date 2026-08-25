# MET-SEMIADD-012 — Proposta A de Política 001

A futura `MET-SEMIADD-012` poderá sugerir somente uma **medida semiaditiva conceitual, revisável e não calculada** quando houver granularidade temporal única definida, sinais agregados de exatamente uma medida de saldo elegível e exatamente uma ordenação temporal elegível sem ambiguidade. A fórmula possível será somente `aggregate eligible_balance across confirmed non_time_dimensions at confirmed time_grain`; a regra não selecionará campos, não determinará se a medida é saldo, não definirá dimensões, período, filtros, partições, tempo de referência, agregação, unidade ou arredondamento, não calculará resultado, não exporá valores e não gerará DAX/M.

Sensibilidade, fórmulas, classificação/grão temporais indefinidos, fato sem grão, conflito, ambiguidade de ordenação, ausência de saldo/tempo ou múltiplas combinações candidatas bloquearão uma futura emissão. A saída terá, no máximo, confiança `0.60`, evidência exclusivamente agregada e pergunta humana bloqueante para confirmar medida de saldo, dimensão temporal, dimensões não temporais, tempo de referência, agregação, população, período, filtros e unidade.

> Esta Proposta A é estritamente não executável. Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção.
