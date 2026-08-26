# ALT-METRIC-006 — Gate de Calibração Draft 001

## Decisão

Com base na autorização explícita de Chris — **“sim autorizado. continue isso logo para finaizarmos essas 95 regras”** — este gate autoriza a `ALT-METRIC-006@0.1.0-provisional.1` exclusivamente no perfil draft. A regra consolida somente uma contagem agregada de sinal de risco de interpretação de métrica já produzida por fonte independente, opaca e autorizada. O classificador não calcula, escolhe ou nomeia medidas, campos, entidades, unidades, populações, períodos, filtros, agregações, relações, fatos ou dimensões; não usa conteúdo de workbook e não gera DAX/M.

## Calibração reproduzível

O golden `alt-metric-draft-golden-v1.json` é estritamente sintético e possui SHA-256 `554f5e3098d5c2bca251cca45c086efd32fb32c02d515db14701ba4eaaea5735`. A avaliação determinística registra `TP=1`, `FP=0` e `FN=0`. O cenário positivo contém somente uma contagem sintética de sinal independente; os cenários negativos cobrem ausência de sinal, confirmação humana, sensibilidade e bloqueios estruturais.

## Guardas e limites

Ausência ou não autorização de sinal, confirmação humana de interpretação, conflito estrutural, sinal de sensibilidade ou erro contratual suprimem o finding. O pipeline de workbook fixa `independent_metric_risk_signal_count=0` porque não há fonte independente autorizada para esse sinal; portanto, nenhuma detecção real é alegada. A saída, quando exercida apenas em teste sintético, é uma solicitação conceitual de revisão humana com evidência de contagem agregada.

## Bloqueio produtivo

Este gate não autoriza produção, promoção de ambiente, cálculo ou recomendação de métrica. **Produção permanece bloqueada.**

