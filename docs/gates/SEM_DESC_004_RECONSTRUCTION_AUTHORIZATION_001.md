# SEM-DESC-004 — Gate de Reconstrução e Autorização 001

## Decisão

Chris aprovou explicitamente a Proposta A da `SEM-DESC-004` nesta sessão. Fica autorizada a reconstrução de uma implementação provisória de **Nome ou descrição**, limitada ao perfil draft controlado.

## Escopo autorizado

| Elemento | Limite autorizado |
|---|---|
| Vocabulário | Após normalização transitória: `nome`, `descricao` e `descrição` |
| Base mínima | Pelo menos 10 observações não ausentes |
| Tipo físico | Todos os valores não ausentes devem ser textos físicos; nenhum número, data, booleano ou serial Excel |
| Fórmulas | `formula_count = 0` é obrigatório |
| Datas | `recognized_date_count = 0` é obrigatório |
| Distinção | Pelo menos dois valores distintos e `distinct_ratio >= 0.20` |
| Saída | `name_or_description_candidate` no campo canônico `semantic_type` |
| Confiança | `0.70` |
| Revisão humana | Pergunta bloqueante obrigatória |
| Ambiente | Exclusivamente `executable_draft`; produção permanece bloqueada |

## Coordenação obrigatória de privacidade

O cabeçalho `nome` continuará a produzir `personal_data_candidate` pela `SEM-SENS-015`. A nova regra não pode suprimir, alterar ou misturar essa saída: `name_or_description_candidate` pertence a `semantic_classifications`, enquanto a classificação de sensibilidade permanece somente em `sensitivity_classifications`. O mascaramento de cabeçalho e título de aba continua obrigatório e independente.

Nenhum valor, cabeçalho normalizado, token, assinatura, amostra, posição, título de aba, formato de célula ou hash de conteúdo poderá ser persistido, projetado ou usado como evidência. O texto do cabeçalho será avaliado exclusivamente de forma transitória para derivar `header_eligible`.

## Implementação condicionada

A autorização permite somente um profiler imutável e agregado, um classificador determinístico, registro no catálogo semântico, versão de contrato, integração canônica guardada por allowlist, testes unitários e de pipeline, golden dataset sintético, SHA-256, avaliador reprodutível de TP/FP/FN e gate individual de calibração.

Não estão autorizados vocabulário adicional, inferência por conteúdo, comprimento, idioma, frequência, domínio, posição, título de aba ou formatação visual; aprendizado de máquina; decisão automática de entidade, chave, dimensão, relacionamento, métrica ou finalidade de tratamento.

## Rastreabilidade

1. `artifacts/intake/SEM-DESC-004.json`.
2. `docs/rules/SEM_DESC_004_POLICY_PROPOSAL_001.md`.
3. `docs/rules/SEM_DESC_004_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris para a Proposta A nesta sessão.
