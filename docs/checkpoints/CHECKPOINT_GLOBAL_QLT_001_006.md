# Checkpoint Global — QLT-001 a QLT-006

## Escopo e método

Este checkpoint consolida a baseline `PM-MVP-PBI-RULESET-QUALITY-006` v`0.6.0`. A revisão utiliza os artefatos de validação G6.4, o fechamento G6.5, o ruleset cumulativo, as definições materiais das seis regras e os registros de interação já aprovados. O checkpoint é **documental e de governança**: ele não substitui a reexecução futura em golden datasets nem transforma regras em produção.

| Critério | Evidência revisada | Resultado |
|---|---|---|
| Escopo da baseline | Ruleset com seis regras na categoria Qualidade | Conforme |
| Ordem de execução | `QLT-NULL-001` até `QLT-BADDATE-006` | Conforme |
| Contrato de diagnóstico | Versão `1.0.0` | Conforme |
| Contexto de análise | Versão `1.6.0` exigida pela QLT-BADDATE-006 | Conforme, com controle de regressão |
| Estado do ruleset | `draft` | Conforme; produção permanece bloqueada |
| Testes individuais históricos | 61 de 61 aprovados no G6.4 | Conforme |
| Testes de interação históricos | 16 de 16 aprovados no G6.4 | Conforme |
| Ciclos de dependência | Zero no G6.4 | Conforme |
| Próxima regra prevista | `QLT-NUMTEXT-007` | Conforme |

## Coerência, precedência e interação

O conjunto possui precedência explicitamente demonstrada entre `QLT-NULL-001` e `QLT-EMPTYCOL-003`: uma coluna totalmente vazia suprime o finding genérico de nulos quando a regra de coluna vazia é mais específica; em um cenário de chave nula, a regra de nulos pode prevalecer. A combinação de `QLT-NULL-001`, `QLT-MIXTYPE-005` e `QLT-BADDATE-006` também foi exercitada sem supressão indevida quando cada diagnóstico trata um aspecto distinto do mesmo campo.

Os findings devem continuar a conter identificação da regra, severidade, confiança, evidências, recomendação e, quando aplicável, perguntas e informações de supressão. A QLT-BADDATE-006 só conclui sobre invalidez temporal quando existe intenção temporal suficiente e tentativa de parsing, evitando que nulos, vazio estrutural ou ambiguidade interpretável sejam tratados como data inválida.

## Regressão e integridade

O G6.4 registrou a preservação dos hashes das cinco regras anteriores e a ausência de ciclos de dependência. O G6.5 também registrou a revalidação dos artefatos fisicamente disponíveis, sem divergências nesse subconjunto. Nem todos os artefatos do manifest histórico estavam materializados no pacote compartilhado; em especial, o único JSON disponível para QLT-NULL-001 é um exemplo anterior que não corresponde ao hash de baseline G6.4. Portanto, este checkpoint preserva essa limitação de evidência, em vez de inferir nova equivalência de hashes.

| Item de controle | Decisão |
|---|---|
| Alteração silenciosa de regras 001–006 | Proibida |
| Reexecução com golden datasets | Pendente e obrigatória antes de produção |
| Ativação produtiva de qualquer regra | Bloqueada |
| Compatibilidade de contexto | Manter `Analysis Context` v`1.6.0` ou versão posterior compatível |
| Compilados no pacote fonte | Não materializados; sem impacto na decisão documental |

## Dívida técnica preservada

Duas inconsistências de namespace permanecem registradas como dívida técnica: uma referência `sheet.name` na QLT-DUP-002 e uma referência `column.name` na QLT-NULL-001. A decisão deste checkpoint é **não corrigir silenciosamente**. Qualquer normalização deverá ocorrer em uma revisão versionada de hardening, com impacto, testes e revalidação explícitos.

## Decisão do checkpoint

> **Decisão: aprovado com restrições de governança.** A baseline QLT-001 a QLT-006 está coerente para permitir a preparação do blueprint do catálogo e a autorização documental da QLT-NUMTEXT-007. Esta aprovação não habilita produção, não encerra a calibração e não elimina as dívidas técnicas registradas.

O próximo artefato obrigatório é o blueprint congelado das 95 regras. A QLT-NUMTEXT-007 deverá ser implementada somente dentro desse blueprint, obedecendo ao ciclo de escopo, política, contexto, rastreabilidade, evidência, outcome, testes, integração, regressão e fechamento.

## Referências internas

| Referência | Artefato de origem |
|---|---|
| G6.4 | `g6.4-validation-report.json` |
| G6.5 | `g6.5-closure-report.json` |
| Ruleset cumulativo | `quality-ruleset-v0.6.0.json` |
| Baseline das regras | `qlt_dup_002.json` a `qlt_baddate_006.json`; QLT-NULL-001 canônica ainda precisa ser recuperada |
