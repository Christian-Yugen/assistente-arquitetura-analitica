# MET-AVG-005 — Proposta A de Política 001

A futura `MET-AVG-005` poderá sugerir somente uma **média conceitual revisável** quando existir exatamente um candidato agregado de quantidade/moeda não sensível, grão único definido, 20+ linhas e duas ou mais colunas. Ela não calcula média, não seleciona medida ou unidade, não expõe valores e não gera DAX/M.

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade e zero/múltiplos candidatos bloqueiam. A saída futura terá no máximo confiança 0,60, fórmula `AVERAGE(eligible_measure)` e pergunta humana bloqueante sobre medida, unidade, população e filtros.

> Esta política não autoriza perfil, classificador, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.
