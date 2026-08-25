# REL-MANYMANY-004 — Gate de Autorização de Reconstrução 001

## Decisão registrada

Chris aprovou explicitamente a **Proposta A** da `REL-MANYMANY-004` nesta sessão. Este gate sela a política escolhida e autoriza exclusivamente a preparação controlada do escopo de reconstrução. **Ele não autoriza escrever, integrar ou executar lógica da regra.** Uma autorização explícita posterior de Chris será obrigatória antes de qualquer implementação draft.

## Escopo selado para eventual reconstrução

| Elemento | Limite aprovado na Proposta A |
|---|---|
| Unidade de análise | Um par opaco de abas distintas, sem nomes, títulos, cabeçalhos ou valores. |
| Classificações antecedentes | Uma dimensão padrão draft e um fato transacional ou periódico draft. |
| Chave da dimensão | Exatamente uma chave física elegível, não sensível, completa e não única, reduzida a sinais agregados. |
| Referência do fato | Exatamente uma referência física elegível, não sensível, completa e não única, reduzida a sinais agregados. |
| Cobertura referencial | Cobertura agregada integral calculada somente de forma transitória em memória. |
| Direção | Exatamente uma direção elegível entre as abas. |
| Exclusões | Fórmulas, sensibilidade, incompletude, cobertura parcial ou zero, 1:1, autorreferência, dimensão calendário, fato sem granularidade, classificação indefinida, conflito ou ambiguidade bloqueiam. |
| Saída eventual | Hipótese `many_to_many_relationship_candidate`, sem criar relação, tabela ponte ou direção de filtro. |
| Confiança eventual | `0.75`. |
| Revisão humana | Pergunta bloqueante obrigatória. |
| Ambiente futuro | Somente `executable_draft`; produção permanece bloqueada. |

## Privacidade e limites

Qualquer perfil futuro poderá reter somente contagens e booleanos agregados por par: linhas observadas, chaves e referências elegíveis, completude, unicidade, cobertura referencial, direções, fórmulas, sensibilidade, conflito e ambiguidade. A comparação transitória não poderá projetar, persistir ou expor títulos de abas, cabeçalhos, valores, posições, pares correspondentes, frequências individuais, exemplos, chaves, identificadores, hashes de conteúdo ou fórmulas.

Não são autorizadas inferência por semelhança livre de nomes, sinônimos, contexto externo, aprendizado de máquina, confirmação de chave primária ou estrangeira, recomendação de tabela ponte, direção final de filtro, decisão de modelo, alteração de dados ou modificação dos controles de mascaramento. A `SEM-SENS-015`, o mascaramento e `sensitivity_classifications` permanecem independentes e obrigatórios.

## Bloqueios remanescentes

Antes de código ou ativação draft, devem ocorrer cumulativamente: autorização explícita posterior de Chris para iniciar a implementação; perfil privado imutável; classificador determinístico; registro; versão contratual; integração canônica protegida por catálogo; testes unitários, limítrofes, de privacidade, contrato e pipeline; golden dataset sintético; manifesto SHA-256; avaliador reproduzível; calibração TP/FP/FN e gate individual de calibração.

Nenhum desses itens foi iniciado ou é autorizado por este gate. A produção permanece bloqueada.

## Rastreabilidade

1. `artifacts/intake/REL-MANYMANY-004.json`.
2. `docs/rules/REL_MANYMANY_004_POLICY_PROPOSAL_001.md`.
3. `docs/rules/REL_MANYMANY_004_LOGICAL_SPEC_PROPOSAL_001.md`.
4. Aprovação explícita de Chris: “sim, continue com a proposta A que esta aprovada”.
