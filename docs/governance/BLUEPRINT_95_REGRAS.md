# Blueprint Congelado das 95 Regras

O blueprint fixa a distribuição, a estrutura obrigatória e o ciclo de vida do catálogo antes da expansão do conjunto de regras. O artefato canônico é `PM-MVP-PBI-CATALOG-95` v`1.0.0`, em estado `frozen_structure`. Ele não inventa políticas de negócio para regras que ainda não foram autorizadas; por isso, os 88 slots sem especificação permanecem reservados até que tenham objetivo, condição, evidência e testes aprovados.

| Categoria | Prefixo de namespace | Slots | Estado atual |
|---|---|---:|---|
| Qualidade | `QLT` | 15 | Seis regras na baseline, QLT-007 autorizada para especificação e oito slots reservados. |
| Tipagem semântica | `SEM` | 15 | Slots reservados. |
| Fato e dimensão | `FDM` | 20 | Slots reservados. |
| Relacionamentos | `REL` | 10 | Slots reservados. |
| Métricas | `MET` | 15 | Slots reservados. |
| Alertas | `ALT` | 10 | Slots reservados. |
| Granularidade | `GRN` | 10 | Slots reservados. |
| **Total** | — | **95** | **Seis regras existentes e uma autorizada para especificação.** |

Cada entrada deverá obrigatoriamente definir identificador, categoria, nome, objetivo, escopo, entradas, condição, exclusões, evidências, severidade, confiança, outcomes, perguntas, recomendação, supressão, precedência, dependências, requisitos, paths de contexto, testes, expectativa de golden dataset e status. A estrutura executável é mantida em `shared/rules/catalogBlueprint.ts` e protegida por teste unitário.
