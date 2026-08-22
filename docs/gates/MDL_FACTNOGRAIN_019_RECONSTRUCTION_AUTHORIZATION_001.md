# MDL-FACTNOGRAIN-019 — Gate de Autorização de Reconstrução 001

## Decisão registrada

Chris aprovou explicitamente a **Proposta A** da `MDL-FACTNOGRAIN-019` nesta sessão. Este gate sela a política escolhida e autoriza exclusivamente a preparação controlada do escopo de reconstrução. **Ele não autoriza escrever, integrar ou executar lógica da regra.** Uma autorização explícita posterior de Chris será obrigatória antes de qualquer implementação draft.

## Escopo selado para eventual reconstrução

| Elemento | Limite aprovado na Proposta A |
|---|---|
| Base | Pelo menos 20 linhas observadas na aba. |
| Medidas | Uma ou mais medidas numéricas físicas elegíveis, reduzidas a contagem agregada. |
| Sinais de fato | Presença agregada de sinais de fato já produzidos pelo pipeline, sem reinspecionar conteúdo. |
| Granularidade ausente | Zero hipóteses de granularidade ativas, contadas somente como sinal agregado. |
| Exclusões | Fórmulas, marcador sensível, tabela dimensional candidata, temporalidade incompatível, menos de 20 linhas ou qualquer ambiguidade bloqueiam a saída. |
| Saída eventual | Classificação `fact_without_defined_grain_candidate`. |
| Confiança eventual | `0.75`. |
| Revisão humana | Pergunta bloqueante obrigatória para definição da granularidade. |
| Ambiente futuro | Somente `executable_draft`; produção permanece bloqueada. |

## Privacidade e limites

Qualquer perfil futuro poderá reter somente sinais agregados: total de linhas observadas, contagem de medidas elegíveis, presença de sinais de fato, contagem de hipóteses de granularidade, exclusões, fórmulas e ambiguidades, além da base técnica. A avaliação transitória não poderá projetar ou reter cabeçalhos, índices, valores, rótulos, exemplos, posições, títulos de abas, tokens, fórmulas, hashes de conteúdo, pares de sinais ou frequências por valor.

Não são autorizadas inferência por conteúdo, sinônimos livres, contexto externo, aprendizado de máquina, confirmação de tabela fato, escolha ou confirmação de granularidade, classificação de dimensão, criação de relacionamento, decisão de modelo, alteração de dados ou modificação dos controles de mascaramento. A `SEM-SENS-015`, o mascaramento de dados sensíveis e `sensitivity_classifications` permanecem independentes e obrigatórios.

## Bloqueios remanescentes

Antes de código ou ativação draft, devem ocorrer cumulativamente: uma autorização explícita posterior de Chris para iniciar a implementação; perfil privado imutável; classificador determinístico; registro; versão contratual; integração canônica protegida por catálogo; testes unitários, limítrofes, de privacidade e de pipeline; golden dataset sintético; manifesto SHA-256; avaliador reproduzível; calibração TP/FP/FN e gate individual de calibração.

Nenhum desses itens foi iniciado ou é autorizado por este gate. A produção permanece bloqueada.

## Rastreabilidade

1. `artifacts/intake/MDL-FACTNOGRAIN-019.json`.
2. `docs/rules/MDL_FACTNOGRAIN_019_POLICY_PROPOSAL_001.md`.
3. `docs/rules/MDL_FACTNOGRAIN_019_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris: “sim”.
