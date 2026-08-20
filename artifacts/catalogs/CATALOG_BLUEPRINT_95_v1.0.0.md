# Artefato Canônico — CATALOG_BLUEPRINT_95 v1.0.0

| Campo | Valor |
|---|---|
| Identificador | `PM-MVP-PBI-CATALOG-95` |
| Versão | `1.0.0` |
| Contrato de diagnóstico | `1.0.0` |
| Estado | `frozen_structure` |
| Fonte executável | `shared/rules/catalogBlueprint.ts` |
| Verificação | `shared/rules/catalogBlueprint.test.ts` |

O artefato congela 95 slots, a sua distribuição por categoria e uma estrutura obrigatória por regra. Para evitar a invenção de políticas de negócio, os campos de regras ainda não autorizadas permanecem como placeholders controlados em estado `not_specified`. Cada slot já contém estrutura para entradas, condição, exclusões, evidências, severidade, confiança, outcomes, perguntas, recomendação, supressão, precedência, dependências, paths de contexto, testes e golden datasets.

As regras da baseline são apenas referenciadas como `baseline_reference`; os detalhes canônicos continuam protegidos por seus artefatos e gates de origem. A QLT-NUMTEXT-007 é a única entrada autorizada para receber especificação neste ciclo.
