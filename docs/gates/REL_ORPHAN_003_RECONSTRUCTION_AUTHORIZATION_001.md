# REL-ORPHAN-003 — Gate de Autorização de Reconstrução 001

## Decisão registrada

Chris aprovou explicitamente a **Proposta A** da `REL-ORPHAN-003` nesta sessão. Este gate sela a política escolhida e autoriza exclusivamente a preparação controlada do escopo de reconstrução. **Ele não autoriza escrever, integrar ou executar lógica da regra.** Uma autorização explícita posterior de Chris será obrigatória antes de qualquer implementação draft.

## Escopo selado para eventual reconstrução

| Elemento | Limite aprovado na Proposta A |
|---|---|
| Unidade de análise | Um par opaco de abas distintas, sem projetar nomes, títulos, cabeçalhos, valores ou posições. |
| Classificações antecedentes | Uma dimensão padrão draft e um fato transacional ou periódico draft. |
| Chave da dimensão | Exatamente uma chave física elegível, não sensível, completa e única, já reduzida a sinais agregados. |
| Referência do fato | Exatamente uma referência física elegível, não sensível, completa e não única. |
| Cobertura referencial | Estritamente superior a `0.0` e inferior a `1.0`, com contagem agregada positiva de referências não cobertas, calculada apenas em memória. |
| Direção | Exatamente uma direção elegível entre as abas. |
| Exclusões | Fórmulas, sensibilidade, incompletude, cobertura zero ou integral, nenhuma correspondência, 1:1, muitos-para-muitos, autorreferência, dimensão calendário, fato sem granularidade, classificação indefinida, conflito ou ambiguidade bloqueiam. |
| Saída eventual | Hipótese `orphan_reference_candidate`, sem criar relacionamento ou identificar referências. |
| Confiança eventual | `0.80`. |
| Revisão humana | Pergunta bloqueante obrigatória. |
| Ambiente futuro | Somente `executable_draft`; produção permanece bloqueada. |

## Privacidade e limites

Qualquer perfil futuro poderá reter somente contagens e booleanos agregados por par: linhas, chaves e referências elegíveis, completude, unicidade, cobertura referencial, quantidade agregada de referências não cobertas, direções, fórmulas, sensibilidade, conflito e ambiguidade. A comparação transitória não poderá projetar, persistir ou expor títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores, hashes de conteúdo ou fórmulas.

Não são autorizadas inferência por semelhança livre de nomes, sinônimos, contexto externo, aprendizado de máquina, identificação de valores órfãos, confirmação de chave primária ou estrangeira, criação de relacionamento, direção final de filtro, decisão de modelo, alteração de dados ou modificação dos controles de mascaramento. A `SEM-SENS-015`, o mascaramento de dados sensíveis e `sensitivity_classifications` permanecem independentes e obrigatórios.

## Bloqueios remanescentes

Antes de código ou ativação draft, devem ocorrer cumulativamente: uma autorização explícita posterior de Chris para iniciar a implementação; perfil privado imutável; classificador determinístico; registro; versão contratual; integração canônica protegida por catálogo; testes unitários, limítrofes, de privacidade, contrato e pipeline; golden dataset sintético; manifesto SHA-256; avaliador reproduzível; calibração TP/FP/FN e gate individual de calibração.

Nenhum desses itens foi iniciado ou é autorizado por este gate. A produção permanece bloqueada.

## Rastreabilidade

1. `artifacts/intake/REL-ORPHAN-003.json`.
2. `docs/rules/REL_ORPHAN_003_POLICY_PROPOSAL_001.md`.
3. `docs/rules/REL_ORPHAN_003_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris: “proposta A aprovada”.
