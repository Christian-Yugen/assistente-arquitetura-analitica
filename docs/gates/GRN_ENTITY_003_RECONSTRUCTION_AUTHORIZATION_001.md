# GRN-ENTITY-003 — Gate de Autorização de Reconstrução 001

## Decisão registrada

Chris aprovou explicitamente a **Proposta A** da `GRN-ENTITY-003` nesta sessão. Este gate sela a política escolhida e autoriza exclusivamente a preparação controlada do escopo de reconstrução. **Ele não autoriza escrever, integrar ou executar lógica da regra.** Uma autorização explícita posterior de Chris será obrigatória antes de qualquer implementação draft.

## Escopo selado para eventual reconstrução

| Elemento | Limite aprovado na Proposta A |
|---|---|
| Base | Pelo menos 20 linhas observadas na aba. |
| Marcador de entidade | Exatamente um cabeçalho, normalizado somente em memória, igual a `cliente`, `produto`, `fornecedor`, `colaborador`, `funcionario`, `paciente`, `aluno` ou `conta`. |
| Chave por linha | Exatamente uma hipótese `explicit_key_candidate` já emitida pela `GRN-EXPL-002`, sem reavaliar a coluna. |
| Atributo descritivo | Pelo menos uma classificação prévia de descrição, categoria, localização ou status, contada apenas como sinal agregado. |
| Ausência temporal | Zero datas não competência reconhecidas; competência também não habilita a hipótese. |
| Ausência de evento ou medida | Zero marcadores de evento e zero sinais previamente classificados de quantidade, moeda, percentual, meta ou realizado. |
| Exclusões | Marcador sensível, descritivo, temporal, com fórmula ou tipo físico divergente bloqueia. |
| Ambiguidade | Zero ou mais de um marcador, chave, data, evento ou medida elegível bloqueia a saída. |
| Saída eventual | Hipótese de granularidade `entity_per_row_candidate`. |
| Confiança eventual | `0.75`. |
| Revisão humana | Pergunta bloqueante obrigatória. |
| Ambiente futuro | Somente `executable_draft`; produção permanece bloqueada. |

## Privacidade e limites

Qualquer perfil futuro poderá reter somente sinais agregados: total de linhas observadas, contagens de marcador elegível, chave explícita, atributo descritivo, datas não competência, eventos, medidas, exclusões, fórmulas e ambiguidades, além da base técnica. A avaliação transitória não poderá projetar ou reter cabeçalhos, índices, valores, rótulos, exemplos, posições, títulos de abas, tokens, fórmulas, hashes de conteúdo, pares de sinais ou frequências por valor.

Não são autorizadas inferência por conteúdo, sinônimos livres, contexto externo, aprendizado de máquina, confirmação de entidade de negócio, classificação de dimensão, criação de relacionamento, decisão de modelo, alteração de dados ou modificação dos controles de mascaramento. A `SEM-SENS-015`, o mascaramento de dados sensíveis e `sensitivity_classifications` permanecem independentes e obrigatórios.

## Bloqueios remanescentes

Antes de código ou ativação draft, devem ocorrer cumulativamente: uma autorização explícita posterior de Chris para iniciar a implementação; perfil privado imutável; classificador determinístico; registro; versão contratual; integração canônica protegida por catálogo; testes unitários, limítrofes, de privacidade e de pipeline; golden dataset sintético; manifesto SHA-256; avaliador reproduzível; calibração TP/FP/FN e gate individual de calibração.

Nenhum desses itens foi iniciado ou é autorizado por este gate. A produção permanece bloqueada.

## Rastreabilidade

1. `artifacts/intake/GRN-ENTITY-003.json`.
2. `docs/rules/GRN_ENTITY_003_POLICY_PROPOSAL_001.md`.
3. `docs/rules/GRN_ENTITY_003_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris: “Proposta A”.
