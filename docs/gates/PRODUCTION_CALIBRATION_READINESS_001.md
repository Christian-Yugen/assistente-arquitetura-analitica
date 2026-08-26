# Prontidão para Calibração Produtiva — 001

**Estado:** inventário e proposta documental; não autoriza executar calibração produtiva, coletar dados ou promover produção.

## Evidência atual

O projeto possui manifestos golden e gates individuais do perfil draft. A auditoria local encontrou **75 manifestos**, dos quais **38** declaram `synthetic_only=true` e **54** declaram explicitamente `production_authorized=false`. Esses números descrevem formatos de manifesto; não comprovam cobertura produtiva por regra.

O avaliador consolidado `CAL-QUALITY-DRAFT-001` exercita nove cenários sintéticos apenas para `QLT-NUMTEXT-007` e `QLT-NULL-001`, registra `mismatch_count=0` e decisão `calibrated_for_draft`, mas declara `production_status=blocked`. O Gate MVP também registra que a calibração atual não usa dados reais nem cobre todas as categorias.

## Limitações impeditivas

| Limitação | Consequência | Estado |
|---|---|---|
| Goldens sintéticos e por regra | Não medem variabilidade representativa de ambiente produtivo. | Bloqueia promoção. |
| Cobertura consolidada restrita a duas regras de qualidade | Não produz FP/FN comparáveis para as 95 regras. | Bloqueia promoção. |
| Sem conjunto de avaliação aprovado | Não há base legal, origem, rótulos ou retenção autorizadas para dados de calibração. | Bloqueia coleta e execução. |
| Sem critérios produtivos aprovados | Não há limiares de FP/FN, severidade, estratificação ou decisão de aceite. | Bloqueia decisão de promoção. |

## Proposta documental de conjunto aprovado

Uma futura calibração produtiva deverá ter um intake próprio para um conjunto **mínimo, desidentificado, owner-scoped e aprovado**, sem dados crus em logs, artefatos golden ou diagnósticos. O intake deverá registrar finalidade, origem autorizada, método de desidentificação, inventário de PII, rótulos humanos, retenção, critérios de destruição e responsável pela aprovação.

As métricas mínimas serão TP, FP e FN por regra, estratificadas por categoria, severidade e tipo de decisão bloqueante. O relatório deverá explicitar cobertura, intervalos ou insuficiência amostral, regras não avaliadas e toda exceção. Ausência de dados, rótulos, cobertura ou aprovação deverá manter a regra e o ambiente **fail-closed**.

## Critérios para um futuro gate

Antes de executar qualquer conjunto não sintético, Chris deverá autorizar explicitamente o intake de calibração, a origem e o processamento. Antes de promover produção, será obrigatório um gate separado que prove: conjunto aprovado e desidentificado; FP/FN por regra e estrato; revisão humana de discordâncias; retenção compatível; E2E provisionado; exclusão física suportada; e decisão formal de risco. Esta proposta não concede nenhuma dessas autorizações.
