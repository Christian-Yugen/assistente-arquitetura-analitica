# MDL-UNDEFINED-020 — Gate de Autorização de Reconstrução 001

## Decisão registrada

Chris aprovou explicitamente a **Proposta A** da `MDL-UNDEFINED-020` nesta sessão. Este gate sela a política residual escolhida e autoriza exclusivamente a preparação controlada de seu escopo de reconstrução. **Ele não autoriza escrever, integrar ou executar lógica da regra.** Uma nova autorização explícita de Chris será obrigatória antes de qualquer implementação no perfil draft.

## Escopo selado para eventual reconstrução

| Elemento | Limite aprovado na Proposta A |
|---|---|
| Base | Pelo menos 20 linhas observadas e duas colunas físicas avaliáveis na aba. |
| Avaliação estrutural | Avaliação de granularidade concluída. |
| Conjunto fechado | Exatamente cinco classificadores de tabela draft autorizados avaliados: fato periódico, fato transacional, fato sem granularidade, dimensão padrão e dimensão calendário. |
| Precedência | Zero hipóteses positivas de classificação de tabela. |
| Conflito e ambiguidade | Zero conflito e zero ambiguidade de classificação. |
| Exclusões | Fórmula nos sinais usados, sensibilidade ou perfil incompleto bloqueiam a saída. |
| Saída eventual | Hipótese residual `table_classification_undefined_candidate`. |
| Severidade eventual | `review_required`. |
| Confiança eventual | `0.60`, somente para o estado operacional de revisão. |
| Revisão humana | Pergunta bloqueante obrigatória sobre finalidade analítica e granularidade pretendida. |
| Ambiente futuro | Somente `executable_draft`; produção permanece bloqueada. |

## Privacidade, coexistência e limites

Qualquer perfil futuro poderá reter somente sinais agregados: linhas observadas, colunas físicas avaliáveis, completude da avaliação, quantidade de classificadores avaliados, quantidade de hipóteses positivas, presença de conflito, ambiguidade, fórmula e sensibilidade. A avaliação transitória não poderá projetar ou reter valores, cabeçalhos, posições, títulos de abas, exemplos, rótulos, datas, identificadores, fórmulas, hashes de conteúdo, identidades de classificadores individuais ou frequências por valor.

Não é autorizada inferência por conteúdo, interpretação de texto livre, sinônimos, contexto externo, aprendizado de máquina, confirmação de fato, dimensão, erro, relevância ou semântica de negócio. A hipótese é estritamente residual: uma classificação positiva tem precedência e uma ambiguidade deve permanecer em revisão humana sem emissão da `MDL-UNDEFINED-020`. A `SEM-SENS-015`, o mascaramento e `sensitivity_classifications` permanecem controles independentes e obrigatórios.

## Bloqueios remanescentes

Antes de código ou ativação draft, devem ocorrer cumulativamente: autorização explícita posterior de Chris para iniciar implementação; perfil privado imutável; classificador determinístico; registro; versão contratual; integração canônica protegida por catálogo; testes unitários, limítrofes, de privacidade e de pipeline; golden dataset sintético; manifesto SHA-256; avaliador reproduzível; calibração TP/FP/FN e gate individual de calibração.

Nenhum desses itens foi iniciado ou é autorizado por este gate. A produção permanece bloqueada.

## Rastreabilidade

1. `artifacts/intake/MDL-UNDEFINED-020.json`.
2. `docs/rules/MDL_UNDEFINED_020_POLICY_PROPOSAL_001.md`.
3. `docs/rules/MDL_UNDEFINED_020_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris: “proposta A aprovada”.
