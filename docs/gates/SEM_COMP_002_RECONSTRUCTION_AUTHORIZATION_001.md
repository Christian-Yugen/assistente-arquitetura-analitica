# SEM-COMP-002 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-COMP-002` nesta sessão. Fica autorizada a reconstrução de uma implementação provisória de **Data de competência**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Vocabulário | Após normalização transitória: `competencia`, `data competencia` e `data de competencia` |
| Base temporal | No mínimo 10 observações não ausentes, todas reconhecidas integralmente pela SEM-DATE-001 |
| Formatos aceitos | Apenas `AAAA-MM-DD`, `DD-MM-AAAA` ou `DD/MM/AAAA` estritamente reconhecidos |
| Fórmulas | `formula_count = 0` é obrigatório |
| Saída | `competence_date_candidate` no campo canônico `semantic_type` |
| Confiança | `0.85` |
| Precedência | Coexiste com `date_generic`; não suprime nem promove automaticamente a SEM-DATE-001 |
| Revisão humana | Pergunta bloqueante obrigatória |
| Ambiente | Exclusivamente `executable_draft`; produção permanece bloqueada |

## Implementação condicionada

A autorização permite reutilizar somente sinais agregados e privados já disponíveis para data e cabeçalho, criar perfil imutável, classificador determinístico, registro semântico, versão de contrato, integração canônica protegida pela allowlist, testes unitários e de pipeline, dataset golden sintético, SHA-256, avaliador reprodutível de TP/FP/FN e gate individual de calibração.

A regra não poderá ser adicionada à allowlist draft até que a calibração individual tenha sido concluída e documentada. A hipótese não determinará período contábil, fiscal, trabalhista ou operacional.

## Limites não autorizados

Não estão autorizados vocabulário além da lista fechada, inspeção ou retenção de valores, datas parciais como `AAAA-MM`, números seriais de Excel, timestamps, inferência por frequência, posição, título de aba, domínio, formatação visual, contexto de outras colunas, conversão de data, alteração de timezone ou decisão automática de modelagem.

O texto do cabeçalho será avaliado apenas transitoriamente para derivar `header_eligible`; não poderá ser serializado, persistido ou projetado. O mascaramento preexistente de cabeçalhos e títulos de abas permanece controle independente e obrigatório.

## Rastreabilidade

1. `artifacts/intake/SEM-COMP-002.json`.
2. `docs/rules/SEM_COMP_002_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_COMP_002_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris para continuar a Proposta A nesta sessão.
