# Autorização e Disponibilidade de Execução E2E — 001

**Estado:** autorização registrada para preparar E2E sintético; execução permanece bloqueada até existir ambiente descartável verificável.

## Autorização registrada

Em 26 de agosto de 2026, Chris autorizou a preparação do ciclo de E2E com a condição de uso exclusivo de identidades e XLSX sintéticos. A autorização não permite dados reais, dados pessoais, dados de clientes, promoção de produção, alteração de regras, alteração de allowlist ou alegação de deleção física.

## Verificação de disponibilidade

A verificação local confirmou que a aplicação de desenvolvimento está acessível e que há configuração de banco disponível. Contudo, o projeto não possui executor E2E instalado, e essa configuração local não comprova uma base separada, descartável e isolada de ambientes produtivos. Portanto, ela não satisfaz a pré-condição de ambiente provisionado definida em `E2E_PROVISIONING_READINESS_001`.

| Critério | Resultado atual | Decisão |
|---|---|---|
| Aplicação de desenvolvimento acessível | Confirmado localmente. | Insuficiente como evidência E2E provisionada. |
| Configuração de banco presente | Confirmada sem expor credencial. | Não prova separação, descarte ou isolamento. |
| Executor E2E instalado | Não confirmado; Playwright e Cypress não estão presentes. | Bloqueia execução automatizada. |
| Banco descartável isolado | Não demonstrado. | Bloqueia criação de identidades sintéticas e execução. |
| Autorização de Chris | Confirmada para preparação sintética. | Não substitui as pré-condições técnicas. |

## Decisão

> A preparação documental está autorizada, mas **nenhum cenário E2E será executado** no ambiente atual.

Antes de instalar uma ferramenta de E2E, criar identities de teste, escrever testes executáveis ou realizar upload sintético, será necessário disponibilizar um ambiente descartável com banco isolado e uma configuração explicitamente não produtiva. Essa mudança deverá receber gate de execução próprio, registrar o executor escolhido, preservar evidências sanitizadas e permanecer limitada ao perfil draft.

Produção continua bloqueada por calibração produtiva, exclusão física indisponível, prova E2E provisionada ausente e os demais critérios do Gate MVP.

## Referências internas

| Artefato | Aplicação |
|---|---|
| `docs/gates/E2E_PROVISIONING_READINESS_001.md` | Pré-condições e cenários E2E sintéticos futuros. |
| `docs/gates/MVP_1_0_READINESS_001.md` | Bloqueio de produção e ausência de prova E2E provisionada. |
| `docs/gates/PHYSICAL_DELETION_AVAILABILITY_001.md` | Limite atual de retenção e inexistência de deleção física. |
