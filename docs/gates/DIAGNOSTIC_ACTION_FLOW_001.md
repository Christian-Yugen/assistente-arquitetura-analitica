# Fluxo de Ação Pós-Diagnóstico — 001

**Estado:** contrato autorizado para o perfil draft; não altera regras, não reprocessa arquivos, não cria fatos, dimensões, relações ou métricas e não promove produção.

## Objetivo

Cada diagnóstico deve explicar ao usuário o que corrigir, quais confirmações humanas ainda faltam e quando uma nova versão do arquivo deve ser analisada. O fluxo converte achados e perguntas existentes em um plano de preparação, sem inferir conteúdo privado ou substituir uma decisão de negócio.

## Resposta humana permitida

Cada pergunta do diagnóstico poderá receber apenas uma decisão enumerada, persistida no escopo do owner e da versão de diagnóstico:

| Decisão | Significado no fluxo |
|---|---|
| `confirmed` | A pessoa responsável confirmou a premissa apresentada. |
| `needs_data_correction` | A premissa indica que o arquivo precisa ser corrigido antes de modelar. |
| `needs_business_review` | A resposta depende de decisão de negócio ou de responsável pelo domínio. |
| `not_applicable` | A pergunta não se aplica ao arquivo ou objetivo informado. |

Não haverá campo livre, anexo, valor de célula, nome de coluna, exemplo, comentário ou PII armazenado como resposta. A resposta não muda automaticamente o motor, a allowlist, o diagnóstico original ou o perfil draft.

## Plano de preparação

O plano será derivado exclusivamente de contagens, severidade e estado das perguntas já presentes no diagnóstico. Ele apresentará, em ordem:

1. **Corrigir achados de qualidade primeiro**, em especial dados ausentes, inconsistências ou estrutura incompleta que afetem qualquer hipótese posterior.
2. **Responder às perguntas de validação**, escolhendo uma das quatro decisões autorizadas para registrar a pendência de negócio ou de dados.
3. **Reenviar uma versão corrigida** quando houver mudança material no arquivo; respostas não são tratadas como edição do CSV/XLSX.
4. **Revisar hipóteses draft** somente quando o diagnóstico posterior trouxer evidência suficiente e perguntas respondidas.

## Isolamento e rejeição fechada

Antes de salvar uma decisão, o servidor verificará que o diagnóstico pertence ao owner autenticado e que o ID da pergunta existe no payload daquele diagnóstico. IDs inexistentes, diagnóstico de outro owner, decisão fora da enumeração ou resposta com campos adicionais serão rejeitados. A resposta será atualizada por pergunta e versão, sem criar cópias concorrentes.

## Limites

O plano não torna um arquivo automaticamente utilizável para produção. Ele é um guia de preparação do perfil draft. Permanecem bloqueados calibração produtiva, E2E provisionado, exclusão física e todos os gates de produção.
