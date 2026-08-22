# MDL-UNDEFINED-020 — Proposta de Política 001

**Regra:** `MDL-UNDEFINED-020` — Classificação indefinida.  
**Estado:** proposta não executável; implementação, catálogo draft e produção bloqueados.  
**Escopo oficial recuperado:** regra P0, por aba, na etapa `table_classification`, dependente de `grain` e com saída `classification_or_table`.[1]

## Lacuna oficial e princípio de segurança

O blueprint oficial exige uma classificação ou proposta de classificação indefinida, mas não determina quando a ausência de uma hipótese positiva pode ser representada de forma segura. A ausência de candidato **não prova** que a aba seja fato, dimensão, erro, irrelevante ou semanticamente desconhecida. Portanto, a proposta não deve transformar a falta de cobertura do motor em uma conclusão sobre o conteúdo da planilha.

Esta política propõe somente um estado operacional de revisão: `table_classification_undefined_candidate`. Ele significa que o conjunto fechado de classificadores draft avaliados não emitiu hipótese positiva, apesar de a avaliação estrutural ter sido completa dentro do escopo autorizado. Não substitui decisão humana, não confirma classificação e não expõe dados de origem.

## Proposta A — classificação indefinida candidata, estritamente residual

Uma aba poderá receber `table_classification_undefined_candidate` somente quando todos os critérios abaixo forem satisfeitos. A classificação é residual: ela só existe depois da avaliação dos classificadores de tabela autorizados, e nunca concorre com uma hipótese positiva ou ambígua.

| Elemento | Política proposta |
|---|---|
| Base mínima | `observed_row_count >= 20` e pelo menos duas colunas físicas avaliáveis |
| Avaliação mínima | Avaliação concluída das cinco hipóteses draft autorizadas: fato periódico, fato transacional, fato sem granularidade, dimensão padrão e dimensão calendário |
| Precedência | Zero hipóteses positivas e zero conflitos ou ambiguidades de classificação no conjunto avaliado |
| Segurança | Sem fórmulas nos sinais usados, sem sinal sensível e sem perfil incompleto |
| Classificação | `table_classification_undefined_candidate` |
| Severidade | `review_required` |
| Confiança | `0.60`, limitada ao estado operacional de revisão e não à semântica da aba |
| Pergunta humana | Obrigatória e bloqueante: “A aba deve permanecer sem classificação automática enquanto você informa sua finalidade analítica e a granularidade pretendida?” |
| Saída | Fragmento canônico `classification_or_table`, com evidências exclusivamente agregadas |

As evidências futuras poderão reter somente contagens e booleanos agregados: linhas observadas, colunas físicas avaliáveis, quantidade de hipóteses de classificação avaliadas, quantidade de hipóteses positivas, presença de conflito, completude de avaliação, fórmulas e sensibilidade. A regra não poderá persistir ou projetar valores, cabeçalhos, posições, títulos de abas, exemplos, frequências por rótulo, datas, identificadores, hashes de conteúdo ou qualquer dado pessoal.

## Exclusões, coexistência e limites

A regra permanecerá silenciosa quando houver menos de 20 linhas, menos de duas colunas físicas avaliáveis, perfil incompleto, fórmula nos sinais usados, sensibilidade, hipótese positiva de classificação, conflito, ambiguidade ou classificador necessário ainda não avaliado. Ela não diagnostica qualidade, não corrige dados, não interpreta texto livre, não sugere relacionamento, não escolhe fatos ou dimensões e não infere granularidade.

Uma hipótese positiva emitida por regra autorizada sempre tem precedência sobre a classificação residual. Do mesmo modo, ambiguidade não deve ser escondida sob o rótulo “indefinida”: a aba precisa continuar em revisão humana, sem emissão desta hipótese. O mascaramento automático e a `SEM-SENS-015` permanecem controles independentes.

## Alternativa B — silêncio com pergunta genérica

Uma alternativa seria não emitir qualquer classificação e apenas solicitar contexto quando não houver candidato positivo. Essa opção reduz ainda mais o risco de interpretação indevida, mas não produz o estado estruturado previsto pelo propósito oficial da regra e dificulta rastrear abas cuja avaliação foi completa, porém inconclusiva. A Proposta A mantém a precisão da alternativa B ao proibir emissão diante de ambiguidade, conflito ou avaliação incompleta.

## Condição de avanço

Esta política não autoriza perfil, classificador, registro, versão de contrato, integração de pipeline, catálogo, testes executáveis, golden dataset, calibração ou produção. O avanço exige aprovação explícita de Chris para a Proposta A, gate de reconstrução, nova autorização específica de implementação, testes e calibração reprodutíveis, gate individual e ativação exclusivamente draft.[2]

## Estado da aprovação

**Proposta A aprovada explicitamente por Chris.** Esta decisão autoriza exclusivamente a formalização do gate de reconstrução. Não autoriza perfil, classificador, registro, contrato, pipeline, catálogo, testes executáveis, golden dataset, calibração ou ativação. A implementação continua dependente do gate de reconstrução e de autorização explícita posterior de Chris.

## Referências internas

[1] `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 60, `MDL-UNDEFINED-020`.

[2] `docs/governance/RULE_DEVELOPMENT_LIFECYCLE_001.md`.
