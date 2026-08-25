# MET-DCOUNT-004 — Proposta A de Política 001

A futura `MET-DCOUNT-004` poderá sugerir somente uma **contagem distinta conceitual revisável** quando existir um único candidato agregado de identificador não sensível, grão único definido, 20+ linhas e duas ou mais colunas. Ela não calcula cardinalidade, não seleciona entidade, não expõe valores/IDs, não gera DAX/M e não altera arquivos.

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito, ambiguidade e zero/múltiplos candidatos bloqueiam. A saída futura terá no máximo confiança 0,60, fórmula `DISTINCTCOUNT(eligible_entity)` e pergunta humana bloqueante sobre a entidade e filtros.

> Esta política não autoriza perfil, classificador, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.
