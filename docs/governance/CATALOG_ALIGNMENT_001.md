# Alinhamento do Catálogo Oficial — CATALOG-ALIGNMENT-001

O documento de prontidão `PM-MVP-PBI-RDY-001 v1.0` foi revisitado como fonte de maior precedência para o catálogo. O alinhamento corrige o namespace local de **FDM** para **MDL**, compatível com os IDs oficiais de fato e dimensão, tais como `MDL-FACTPER-001` e `MDL-UNDEFINED-020`.

| Categoria | Namespace oficial | Slots |
|---|---:|---:|
| Qualidade | `QLT` | 15 |
| Tipagem semântica | `SEM` | 15 |
| Granularidade | `GRN` | 10 |
| Fato e dimensão | `MDL` | 20 |
| Relacionamentos | `REL` | 10 |
| Métricas | `MET` | 15 |
| Alertas | `ALT` | 10 |

O artefato `artifacts/catalogs/official-rule-blueprint-95.json` preserva, sem alteração semântica, os 95 IDs, títulos, propósitos, prioridades, estágios, escopos, dependências, outputs e estados da fonte `PM-MVP-PBI-RULE-BP-001`. A projeção TypeScript em `shared/rules/officialCatalog.ts` é gerada por script rastreável e o registro Python a lê diretamente.

Os IDs dos 95 slots permanecem bloqueados contra execução até que cada política seja especificada, testada e autorizada. As sete regras de referência da fonte são distinguidas de regras executáveis: permanecem como referência de catálogo, sem ativação silenciosa. A QLT-NUMTEXT-007 é a única regra executável no modo draft atual; as demais não recebem condição de negócio nem execução por efeito deste alinhamento.
