# QLT-NUMTEXT-007 — Valores Numéricos Armazenados como Texto

## Propósito

A regra identifica valores que permanecem fisicamente como texto, mas são interpretáveis por uma base numérica canônica estrita. Ela não converte dados e não conclui que uma coluna é métrica: apenas torna o risco visível e pede confirmação quando a incidência pode comprometer classificação, agregação e recomendação.

| Aspecto | Decisão v1.0.0-draft |
|---|---|
| Escopo | Coluna textual ou mista. |
| Pré-condição | Profiling concluído e base `strict_canonical_numeric_string`. |
| Precedência | Executa após QLT-NULL-001, QLT-EMPTYCOL-003 e QLT-MIXTYPE-005. |
| Sobreposição | Complementa QLT-MIXTYPE-005; não substitui seu finding de integridade. |
| Saída | Um finding agregado por coluna e pergunta bloqueante em severidade alta. |
| Privacidade | Não inclui valores brutos, amostras ou conteúdo de células nas evidências. |
| Produção | Bloqueada até golden dataset, regressão e gate de fechamento. |

## Limites provisórios

Uma razão abaixo de 5% gera severidade baixa; de 5% a menos de 50%, média; e 50% ou mais, alta. A confiança começa em 0,90 e é reduzida quando o profiling marca ambiguidade numérica. Esses limiares são hipótese técnica controlada e deverão ser recalibrados em `GD-QLT-NUMTEXT-007`, sem alteração silenciosa da regra.

Quando a severidade é alta, a pergunta solicita que o usuário diferencie medida numérica, identificador/código ou estado desconhecido. A resposta deverá disparar uma nova versão de diagnóstico no futuro pipeline, sempre preservando a linhagem entre a resposta e os findings reavaliados.
