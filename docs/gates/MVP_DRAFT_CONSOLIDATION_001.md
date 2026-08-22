# MVP-DRAFT-CONSOLIDATION-001 — Gate de Consolidação do Fluxo

**Decisão:** aprovado **somente como MVP draft controlado**.  
**Decisão de produção / MVP 1.0:** bloqueada.

O fluxo implementado recebe um workbook `.xlsx` autenticado, executa validações antes da persistência, inspeciona a planilha no servidor, produz o diagnóstico canônico draft por motor Python, persiste os artefatos no escopo do proprietário e remove a referência privada do arquivo ao término. A interface apresenta os estados autenticados, versões do diagnóstico e exportação JSON do diagnóstico selecionado.

| Dimensão | Evidência | Resultado |
|---|---|---|
| Contrato | PM-MVP-PBI-CON-001 reconstruído e validado contra schema/modelos. | Aprovado para draft. |
| Catálogo | Blueprint oficial de 95 regras sincronizado; 40 regras possuem implementação local, allowlist e gates individuais no draft. | Aprovado com execução limitada. |
| Motor | Runner Python, profiling agregado sem valores brutos e teste de workbook real temporário. | Aprovado para draft. |
| Acesso | Procedures autenticados, helpers owner-scoped e provas estruturadas de leitura e escrita. | Aprovado para draft. |
| Retenção | Referência privada removida com auditoria; exclusão física indisponível. | Aprovado apenas como controle compensatório. |
| Privacidade | Sanitização, bloqueio de payload sensível, títulos de abas anonimizados e logs operacionais genéricos. | Aprovado para draft. |
| Interface | Estados de autenticação/mutation, navegação, histórico e exportação JSON testados. | Aprovado para draft. |
| Regressão | `pnpm test`: 43 testes Vitest; `pnpm test:engine`: 30 testes Python; `pnpm check`: aprovado. | Aprovado. |

## Bloqueios de promoção

| Bloqueio | Condição para remoção |
|---|---|
| Catálogo incompleto | Intake, especificação, implementação, testes, golden dataset e gate de cada uma das regras pendentes. |
| Calibração | Golden datasets e avaliação documentada de falsos positivos e falsos negativos. |
| Exclusão física | Operação oficial de deleção em armazenamento, teste owner-scoped e gate de retenção aprovado. |
| Artefato QLT-NULL-001 | Recuperação da fonte canônica e validação de hash de baseline. |
| Banco provisionado | Prova integrada contra banco real, sem inserção de dados de teste via operação destrutiva. |
| Exportação PDF e interpretação LLM | Especificações, controles de privacidade e ciclos próprios de validação. |

## Pendências

Permanecem pendentes a recuperação verificável do artefato canônico QLT-NULL-001, a especificação e autorização formal das regras não executáveis, a construção de golden datasets e a calibração de precisão do motor. A retenção física também continua pendente de uma operação oficial de deleção de objeto, e a validação contra banco provisionado deve ocorrer sem inserir dados de teste por operação destrutiva.

## Próximos passos

1. Submeter `RETENTION-EXCEPTION-001` ao aceite explícito do responsável proposto, sem remover o bloqueio de produção.
2. Recuperar a fonte da QLT-NULL-001 e validar o hash de baseline antes de qualquer novo gate de promoção.
3. Executar o intake formal da próxima regra de qualidade e iniciar somente o ciclo que receba autorização documentada.
4. Definir golden datasets, calibrar o motor e reavaliar os falsos positivos e negativos antes de qualquer ativação produtiva.
5. Quando houver capacidade oficial de exclusão no armazenamento, implementar a deleção física, acrescentar teste owner-scoped e solicitar o gate de retenção.

> Este gate não autoriza a promoção produtiva, não amplia o conjunto de regras executáveis e não substitui os gates formais de cada ciclo de regra.
