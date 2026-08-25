# MET-DOMAIN-013 — Proposta A de Política 001

A futura `MET-DOMAIN-013` poderá sugerir somente uma **métrica de domínio conceitual, revisável e não calculada** quando houver granularidade única definida e exatamente um sinal de domínio já classificado de forma independente, opaca e agregada. A saída futura será somente `domain_metric_conceptual_candidate`; a regra não inferirá domínio a partir de conteúdo privado, não selecionará campos, não definirá fórmula, medida, entidade, unidade, população, período, filtros, agregação ou limite, não calculará resultado, não exporá valores e não gerará DAX/M.

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade, ausência de sinal de domínio ou múltiplos sinais de domínio bloquearão uma futura emissão. A saída terá, no máximo, confiança `0.55`, evidência exclusivamente agregada e pergunta humana bloqueante para confirmar o domínio, objetivo, fórmula, medida, entidade, unidade, população, período, filtros, agregação e limites.

> Esta Proposta A é estritamente não executável. Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção.
