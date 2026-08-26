# ALT-METRIC-006 — Proposta A de Política 001

## Escopo proposto

A `ALT-METRIC-006` poderá, somente se Chris autorizar uma implementação posterior e limitada ao perfil draft, consolidar um ou mais **sinais de risco de interpretação de métrica** que já tenham sido produzidos por fonte independente, autorizada, opaca e agregada. O único resultado admitido seria um finding conceitual de **revisão humana obrigatória**. Ele não afirmará que uma decisão de negócio, uma métrica ou um dashboard está errado.

O sinal futuro deverá ser apenas uma contagem agregada ou uma flag contratada. A regra não poderá extrair, recalcular, correlacionar ou enriquecer esse sinal a partir de workbook, títulos, cabeçalhos, fórmulas, valores, pares de dados, frequência, posição, tabela, dimensão, fato, relação, medida, unidade, população, período, filtro ou agregação.

## Condição e supressão propostas

Uma futura emissão somente seria considerada quando existir ao menos um sinal independente e agregado de risco de interpretação, o contrato estiver válido e não houver indicação de sensibilidade, erro contratual ou incerteza não resolvida sobre classificação, granularidade, fato, dimensão ou relacionamento. Ausência de sinal, sinal não autorizado, mais detalhes do que uma contagem ou flag agregada, dados sensíveis, inconsistência de contrato, conflito estrutural ou qualquer lacuna de pré-condição devem **suprimir** o finding de modo fail-closed.

## Saída restrita

O finding futuro deverá usar linguagem conceptual e revisável, severidade alta apenas como priorização de revisão e uma pergunta humana bloqueante sobre a finalidade analítica, a população, a unidade e a interpretação confirmadas. Não poderá selecionar ou nomear qualquer medida, campo, entidade, unidade, população, período, filtro, agregação ou relação. Não poderá calcular resultado, comparar desempenho, recomendar meta, formular KPI, gerar DAX, gerar Power Query/M, editar dados ou exportar conteúdo.

## Privacidade, segurança e limites

Nenhum dado de workbook será persistido, exibido, logado ou usado para inferência nesta regra. O perfil, se autorizado no futuro, conterá apenas contagens e flags agregadas; identidades, textos, valores, exemplos, posições, pares e frequências individuais permanecem proibidos. O golden dataset deverá ser estritamente sintético e a produção continuará bloqueada mesmo após eventual ativação draft.

## Estado de autorização

Esta Proposta A é documental e não executável, registrada sob `PROPOSAL-A-APPROVAL-DELEGATION-001` sem mudança material do padrão conservador já aprovado. Ela **não** autoriza perfil, classificador, registro, contrato, pipeline, allowlist, teste executável, golden, calibração ou promoção. Qualquer código executável requer uma autorização nova e explícita de Chris.
