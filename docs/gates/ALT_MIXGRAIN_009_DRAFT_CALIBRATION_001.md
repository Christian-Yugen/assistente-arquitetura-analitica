# ALT-MIXGRAIN-009 — Gate de Calibração Draft 001

## Decisão

Com base na autorização explícita de Chris — **“ok. continue o desenvolvimento, autorizado”** — este gate autoriza a `ALT-MIXGRAIN-009@0.1.0-provisional.1` exclusivamente no perfil draft. A regra consolida somente uma contagem agregada de sinal de mistura de granularidades já produzida por fonte independente, opaca e autorizada. O classificador não infere, calcula, seleciona, combina ou separa granularidades, entidades, eventos, chaves, fatos, dimensões, medidas, campos, unidades, populações, períodos, filtros, agregações ou relações; não usa conteúdo de workbook e não gera DAX/M.

## Calibração reproduzível

O golden `alt-mixgrain-draft-golden-v1.json` é estritamente sintético e possui SHA-256 `5cec12d4ac12c12f4e7601524b72d0c995695553c88b2371fcf88fc5bb3dba71`. A avaliação determinística registra `TP=1`, `FP=0` e `FN=0`. O cenário positivo contém somente uma contagem sintética de sinal independente; os cenários negativos cobrem ausência de sinal, confirmação humana, sensibilidade e bloqueios estruturais.

## Guardas e limites

Ausência ou não autorização de sinal, confirmação humana de granularidade única, conflito estrutural, sinal de sensibilidade ou erro contratual suprimem o finding. O pipeline de workbook fixa `independent_mixed_grain_signal_count=0` porque não há fonte independente autorizada para esse sinal; portanto, nenhuma detecção real é alegada. A saída, quando exercida apenas em teste sintético, é uma solicitação conceitual de revisão humana com evidência de contagem agregada.

## Bloqueio produtivo

Este gate não autoriza produção, promoção de ambiente, inferência de granularidade ou recomendação de modelagem. **Produção permanece bloqueada.**

