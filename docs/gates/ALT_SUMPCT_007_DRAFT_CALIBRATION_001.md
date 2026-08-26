# ALT-SUMPCT-007 — Gate de Calibração Draft 001

## Decisão

Com base na autorização explícita de Chris — **“sim, aprovado vamos acelerar que eu quero colocar esse projeto em produção”** — este gate autoriza a `ALT-SUMPCT-007@0.1.0-provisional.1` exclusivamente no perfil draft. A regra consolida somente uma contagem agregada de sinal de risco na soma de percentuais já produzida por fonte independente, opaca e autorizada. O classificador não detecta, calcula, soma, compara, corrige ou pondera percentuais e não escolhe medidas, campos, entidades, unidades, populações, períodos, filtros, agregações, relações, fatos ou dimensões; não usa conteúdo de workbook e não gera DAX/M.

## Calibração reproduzível

O golden `alt-sumpct-draft-golden-v1.json` é estritamente sintético e possui SHA-256 `71ffb48513d1300c6b9ec16ceb7cde714f6f9aaa7bf438a16cac5d94186847cc`. A avaliação determinística registra `TP=1`, `FP=0` e `FN=0`. O cenário positivo contém somente uma contagem sintética de sinal independente; os cenários negativos cobrem ausência de sinal, confirmação humana, sensibilidade e bloqueios estruturais.

## Guardas e limites

Ausência ou não autorização de sinal, confirmação humana da composição percentual, conflito estrutural, sinal de sensibilidade ou erro contratual suprimem o finding. O pipeline de workbook fixa `independent_percentage_sum_risk_signal_count=0` porque não há fonte independente autorizada para esse sinal; portanto, nenhuma detecção real é alegada. A saída, quando exercida apenas em teste sintético, é uma solicitação conceitual de revisão humana com evidência de contagem agregada.

## Bloqueio produtivo

Este gate não autoriza produção, promoção de ambiente, cálculo, soma ou recomendação de percentuais. **Produção permanece bloqueada.**

