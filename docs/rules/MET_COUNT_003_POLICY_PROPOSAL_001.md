# MET-COUNT-003 — Proposta A de Política 001

A futura `MET-COUNT-003` poderá emitir apenas uma **recomendação conceitual revisável** de contagem para uma aba opaca com grão único definido, 20+ linhas e duas ou mais colunas físicas. Ela não determina a entidade contada, não conta registros, não seleciona campo, não gera DAX/Power Query nem modifica arquivos.

Sensibilidade, fórmulas, classificação/grão indefinidos, fato sem grão, conflito e ambiguidade bloqueiam. A saída futura terá confiança máxima de 0,60, fórmula conceitual `COUNT(eligible_entity)` e pergunta humana bloqueante sobre o que representa a entidade e quais filtros se aplicam.

> Esta política não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, testes executáveis, calibração ou produção.
