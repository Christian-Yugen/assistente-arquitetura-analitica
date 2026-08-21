# QLT-MIXTYPE-005 — Especificação Lógica Proposta 001

**Estado:** proposta para revisão humana; não é especificação autorizada para execução.  
**Política associada:** `QLT_MIXTYPE_005_POLICY_PROPOSAL_001.md`.

## Contrato de entrada proposto

O avaliador receberá exclusivamente um perfil agregado de coluna. O perfil pretendido não reterá valores, posições, nome da aba, nome da coluna, amostras, fórmulas nem conteúdos serializáveis.

| Campo | Tipo | Semântica |
|---|---|---|
| `non_empty_value_count` | inteiro não negativo | Valores que não pertencem às classes de ausência. |
| `boolean_count` | inteiro não negativo | Valores booleanos físicos observados. |
| `numeric_count` | inteiro não negativo | Números físicos observados, exceto booleanos. |
| `text_count` | inteiro não negativo | Textos não vazios que não sejam cadeias numéricas canônicas. |
| `temporal_count` | inteiro não negativo | Datas e horas físicas observadas. |
| `unsupported_count` | inteiro não negativo | Tipos não classificados, fórmulas ou objetos que esta versão deve excluir. |
| `normalization_basis` | literal versionado | Base técnica aplicada às contagens e exclusões. |

## Algoritmo proposto

1. Excluir do perfil todas as classes de ausência já definidas pelo profiler compartilhado.
2. Remover cadeias numéricas canônicas do grupo textual para evitar a duplicação com `QLT-NUMTEXT-007`.
3. Formar grupos candidatos entre `boolean`, `numeric`, `text` e `temporal` com contagem igual ou superior a dois.
4. Declarar a regra aplicável somente se `non_empty_value_count >= 5` e houver pelo menos dois grupos candidatos.
5. Emitir no máximo um finding agregado por coluna aplicável, com severidade determinada pela participação do menor grupo candidato: `low` para menos de 10%, `medium` para 10% a menos de 30% e `high` para 30% ou mais.
6. Produzir pergunta de validação somente para `medium` e `high`; a pergunta não exibirá o identificador da coluna nem conteúdo de célula.

## Invariantes obrigatórios

O avaliador deverá ser determinístico, não mutar o workbook e não invocar IA. Toda evidência deverá ser numérica e agregada. O finding deverá utilizar `rule_id = QLT-MIXTYPE-005`, categoria `quality`, escopo canônico por coluna e uma versão de regra explicitamente registrada. O contrato canônico continuará responsável por validar o objeto resultante.

O perfil deverá satisfazer, antes da avaliação: a soma das contagens de grupos conhecidos não pode exceder `non_empty_value_count`; nenhuma contagem pode ser negativa; e `normalization_basis` deve ser exatamente a base versionada autorizada. Se uma dessas condições não for satisfeita, a regra não deverá emitir finding.

## Casos planejados para testes e calibração, se aprovados

| Caso | Resultado esperado |
|---|---|
| 8 números, 3 textos não numéricos | Finding de severidade `medium`. |
| 5 booleanos, 5 datas físicas | Finding de severidade `high`. |
| 9 números, 1 texto | Sem finding, por minoria abaixo da base conservadora. |
| 6 números, 4 cadeias numéricas canônicas | Sem finding nesta regra; evidência delegada à QLT-NUMTEXT-007. |
| Ausências e textos em branco sem valores materiais | Sem finding. |
| Perfil com base de normalização divergente | Sem finding. |

> A especificação só poderá ser renomeada para um artefato de reconstrução e usada para código após aprovação explícita de Chris para a Opção A da política correspondente.
