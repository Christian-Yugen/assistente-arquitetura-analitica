# REL-NONUNIQ-002 — Gate de Calibração Draft 001

## Decisão

O gate `REL-NONUNIQ-002-DRAFT-CALIBRATION-001` autoriza exclusivamente a promoção da `REL-NONUNIQ-002@0.1.0-provisional.1` para o perfil `executable_draft`, depois da Proposta A aprovada por Chris, do gate de reconstrução, da autorização específica posterior de implementação e da evidência sintética abaixo. **Ele não autoriza produção.**

## Evidência reproduzível

| Elemento | Evidência verificada |
|---|---|
| Dataset | `GD-REL-NONUNIQ-002-001`, exclusivamente sintético e sem nomes, valores, cabeçalhos ou pares de origem. |
| Arquivo | `artifacts/golden/rel-nonuniq-draft-golden-v1.json`. |
| SHA-256 | `95bcbca0b7e9a180d13abb1f77fa4c66d638bf481a4933007b710ce4c7f36929`. |
| Avaliador | `engine/calibration/evaluate_rel_nonuniq_draft_golden.py`. |
| Resultado | 3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos. |
| Cobertura negativa | Fórmulas, sensibilidade, incompletude, cobertura parcial, autorreferência, dimensão calendário, classificação indefinida, fato sem grão, conflitos, 1:1, N:N, ambiguidade, cardinalidade/direção não elegíveis e chave única. |

## Limites de ativação

A ativação draft poderá produzir somente `one_side_key_non_unique_candidate`, confiança `0.80`, severidade `warning`, evidências agregadas e pergunta humana bloqueante. O perfil e a saída não podem revelar títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores ou hashes de conteúdo.

O mascaramento e a `SEM-SENS-015` continuam controles independentes: qualquer sinal sensível deve bloquear a hipótese, mesmo que a condição de não unicidade agregada esteja presente. A regra não identifica a chave, não confirma duplicidade de negócio, não seleciona correção, não cria relacionamento e não altera dados ou o modelo Power BI.

## Produção bloqueada

Este gate não remove os bloqueios de produção, que continuam dependentes da calibração integral do motor, dos demais ciclos governados e do Gate MVP 1.0 produtivo; **a produção permanece bloqueada**. A REL-NONUNIQ-002 permanece uma experiência controlada em draft com confirmação humana obrigatória.
