# SEM-ID-003 — Especificação Lógica Proposta 001

**Estado:** rascunho não executável.

Após a política ser aprovada, o perfil por coluna deverá conter somente: `observed_count`, `non_missing_count`, `distinct_non_missing_count`, `non_missing_ratio`, `distinct_ratio`, `header_signal`, `physical_type_eligible`, `formula_present`, `sensitive_header`, `basis`. Durante o profiling, contagens e assinaturas temporárias podem existir apenas em memória; ao finalizar, o acumulador deve limpar assinaturas e não conservar valores, hashes, cabeçalhos, posições ou títulos de abas.

O classificador deverá falhar fechado. Só produzirá a classificação quando todos os critérios da Proposta A forem verdadeiros. A evidência deve distinguir `individually_unique` de `component_eligible`, sem transportar a identidade de coluna no perfil. A projeção deverá reutilizar `semantic_classifications`, já opcional no contrato canônico, e gerar uma pergunta humana rastreável.

Para a GRN-COMP-001, somente classificações `identifier` vigentes, produzidas por esta regra e marcadas como `component_eligible`, poderão entrar na seleção de pares. A regra de granularidade seguirá mantendo seu limite de dez pares e a confirmação humana obrigatória.
