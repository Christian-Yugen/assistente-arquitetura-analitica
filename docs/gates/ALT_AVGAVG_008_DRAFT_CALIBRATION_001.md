# ALT-AVGAVG-008 — Gate de Calibração Draft 001

## Decisão

Com base na autorização explícita de Chris — **“dim, autorizado”** — este gate autoriza a `ALT-AVGAVG-008@0.1.0-provisional.1` exclusivamente no perfil draft. A regra consolida somente uma contagem agregada de sinal de risco em média de médias já produzida por fonte independente, opaca e autorizada. O classificador não detecta, calcula, recomputa, pondera, compara ou escolhe médias, pesos, denominadores, tamanhos de grupo, medidas, campos, entidades, unidades, populações, períodos, filtros, agregações, relações, fatos ou dimensões; não usa conteúdo de workbook e não gera DAX/M.

## Calibração reproduzível

O golden `alt-avgavg-draft-golden-v1.json` é estritamente sintético e possui SHA-256 `e64594ed197e96848bd0fe5ead4692ea726b8b5280849d12b8ecc1e2173110fe`. A avaliação determinística registra `TP=1`, `FP=0` e `FN=0`. O cenário positivo contém somente uma contagem sintética de sinal independente; os cenários negativos cobrem ausência de sinal, confirmação humana, sensibilidade e bloqueios estruturais.

## Guardas e limites

Ausência ou não autorização de sinal, confirmação humana da composição de médias, conflito estrutural, sinal de sensibilidade ou erro contratual suprimem o finding. O pipeline de workbook fixa `independent_average_of_averages_risk_signal_count=0` porque não há fonte independente autorizada para esse sinal; portanto, nenhuma detecção real é alegada. A saída, quando exercida apenas em teste sintético, é uma solicitação conceitual de revisão humana com evidência de contagem agregada.

## Bloqueio produtivo

Este gate não autoriza produção, promoção de ambiente, cálculo, ponderação ou recomendação de médias. **Produção permanece bloqueada.**

