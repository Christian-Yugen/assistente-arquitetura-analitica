# MET-PCTDELTA-009 — Proposta A de Política 001

A futura `MET-PCTDELTA-009` poderá sugerir somente uma **variação percentual conceitual, revisável e não calculada** quando houver granularidade única definida, sinais agregados de exatamente uma medida realizada e uma referência elegíveis e confirmação agregada de que a referência não é zero. A fórmula possível será somente `((eligible_actual - eligible_baseline) / eligible_baseline) * 100`; a regra não selecionará campos, não determinará período, unidade, população, filtros, convenção de sinal ou arredondamento, não calculará resultado, não exporá valores e não gerará DAX/M.

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade, referência zero, ausência de qualquer componente ou múltiplas combinações candidatas bloquearão uma futura emissão. A saída terá, no máximo, confiança `0.60`, evidência exclusivamente agregada e pergunta humana bloqueante para confirmar medida realizada, referência, convenção percentual, unidade, população, período e filtros.

> Esta Proposta A é estritamente não executável. Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, golden dataset, calibração ou produção.
