# Requisitos de Ambiente E2E Sintético — 001

**Estado:** especificação de provisionamento; não cria ambiente, banco, armazenamento, credenciais, identidades, uploads ou execução E2E.

## Objetivo

Um ambiente E2E separado permitirá comprovar o fluxo completo do MVP draft sem usar a base, o armazenamento, as credenciais ou os usuários do ambiente atual. Ele deve ser descartável, rastreável e capaz de executar apenas fixtures XLSX sintéticas, mantendo a produção bloqueada.

## Isolamento obrigatório

| Domínio | Requisito verificável | Evidência sanitizada exigida |
|---|---|---|
| Aplicação | Projeto ou implantação de teste com identificador próprio e configuração explicitamente não produtiva. | Identificador opaco do ambiente e estado `test`. |
| Banco | Instância ou schema exclusivo; nenhuma URL, tabela ou migração compartilhada com o ambiente atual. | Confirmação de separação, sem expor URL ou credencial. |
| Armazenamento | Namespace, bucket ou prefixo dedicado ao teste; nenhum objeto de usuário real. | Prefixo opaco e contagem agregada de objetos sintéticos. |
| Segredos | Credenciais exclusivas de teste, sem reutilizar segredo de produção. | Declaração de rotação/isolamento, sem valores. |
| Identidade | Dois owners de teste identificados por IDs opacos e sem correspondência com pessoas reais. | Apenas os dois IDs opacos e o resultado do teste de isolamento. |
| Dados | Workbooks criados sinteticamente, com hash verificável e sem PII, cabeçalhos ou valores reais. | Hash, versão de fixture e contagens agregadas. |
| Descarte | Janela de expiração e procedimento de encerramento; remover referências não será declarada como deleção física. | Data de expiração e resultado agregado do encerramento. |

## Critérios de aceite antes de executar E2E

O ambiente somente poderá ser aceito quando todos os domínios acima forem demonstrados. Também deverá existir executor E2E instalado e versionado, com evidência de que a execução aponta para o ambiente identificado como teste. Qualquer ausência, compartilhamento, dado não sintético, evidência não sanitizada ou incerteza sobre isolamento mantém a execução **fail-closed**.

## Limites da plataforma atual

O projeto atual possui aplicação local acessível e configuração de banco, mas não demonstra uma segunda implantação, banco separado, armazenamento separado, credenciais próprias, identidades sintéticas ou executor E2E instalado. Esses limites impedem que o ambiente E2E seja criado dentro deste ciclo somente por código do aplicativo.

Para provisionar de forma válida, a plataforma deverá oferecer ou Chris deverá disponibilizar um projeto/implantação de teste com os domínios isolados listados. Nenhuma cópia manual de credencial, banco ou objeto do ambiente atual será utilizada como atalho.

## Verificação de via de provisionamento

Em 26 de agosto de 2026, a configuração disponível do projeto foi inspecionada sem alterar conectores ou segredos. Ela não expôs integração, ambiente ou comando suportado de provisionamento E2E/WebDev separado. Portanto, não há via verificável para criar o ambiente isolado a partir deste ciclo. A ausência da via não autoriza reutilizar a aplicação local, o banco atual ou qualquer armazenamento existente como substituto.

O desbloqueio requer uma capacidade explícita de provisionamento de projeto/implantação de teste ou a disponibilização de um ambiente separado por Chris. Até então, a tarefa de preparar e executar cenários E2E permanece aberta e a produção continua bloqueada.

## Bloqueio de automação verificado

Chris autorizou explicitamente a criação de E2E real em ambiente isolado, exclusivamente com dados sintéticos. Para verificar a automação necessária, a integração de navegador disponível foi habilitada e consultada. A sessão informou que o navegador exigido para automação não estava instalado. A interface exposta não ofereceu operação oficial de instalação; a operação de instalação indicada pela própria sessão também não foi disponibilizada.

Essa combinação impede a execução de navegador neste ciclo. O projeto não instalará navegador manualmente, não executará comandos não suportados de automação e não substituirá o ambiente isolado pelo ambiente local. O E2E permanece **fail-closed** até que a plataforma ofereça, simultaneamente, navegador de automação funcional e implantação isolada verificável.

## Gate de execução posterior

Quando o ambiente existir, o gate de execução deverá registrar: identificador opaco do ambiente, versão do executor, hashes das fixtures, IDs opacos dos dois owners, janela de descarte, resultados dos cenários `E2E-SYN-001` a `E2E-SYN-006`, ausência de conteúdo privado nas evidências e decisão limitada ao perfil draft. Aprovação dos cenários não libera produção.

## Referências internas

| Artefato | Aplicação |
|---|---|
| `docs/gates/E2E_PROVISIONING_READINESS_001.md` | Define os cenários sintéticos futuros e o bloqueio de produção. |
| `docs/gates/E2E_EXECUTION_AUTHORIZATION_001.md` | Registra a autorização de Chris e a indisponibilidade técnica anterior. |
| `docs/gates/PHYSICAL_DELETION_AVAILABILITY_001.md` | Impede alegação de deleção física no encerramento. |
