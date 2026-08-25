# MET-RATE-007 — Proposta A de Política 001

A futura `MET-RATE-007` poderá sugerir apenas uma **taxa conceitual revisável** diante de granularidade única definida e de sinais agregados para exatamente um numerador e um denominador elegíveis. Ela não escolhe campos, não calcula taxa ou percentual, não define população/unidade/filtros, não expõe valores e não gera DAX/M.

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade, denominador ausente ou múltiplas combinações candidatas bloqueiam. A saída futura terá no máximo confiança 0,60, fórmula `eligible_numerator / eligible_denominator` e pergunta humana bloqueante sobre numerador, denominador, unidade, população e filtros.

> Esta política não autoriza perfil, classificador, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.
