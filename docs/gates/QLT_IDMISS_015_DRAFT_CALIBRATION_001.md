# QLT-IDMISS-015-DRAFT-CALIBRATION-001

**Data da decisão:** 20 de agosto de 2026.  
**Regra:** `QLT-IDMISS-015 — Identificadores incompletos`.  
**Versão:** `0.1.0-provisional.1`.  
**Escopo de liberação:** somente `draft`.  
**Decisão:** **aprovada para a allowlist draft; produção bloqueada.**

## Pré-condições verificadas

| Controle | Evidência | Resultado |
|---|---|---|
| Política autorizada | `QLT-IDMISS-015-RECONSTRUCTION-AUTHORIZATION-001`, com a Proposta A aprovada por Chris. | Aprovado. |
| Perfil privado | `IdentifierCompletenessProfile` mantém somente elegibilidade, contagens e razões agregadas; não mantém cabeçalhos, identificadores, valores, hashes, assinaturas, posições ou títulos de aba. | Aprovado. |
| Vocabulário fechado | A regra só admite, após normalização técnica do cabeçalho, `id`, `codigo`, `cod`, `chave`, `matricula`, `cpf`, `cnpj`, `numero` e `num`. | Aprovado. |
| Sinais e exclusões | Observa somente ausência privada e duplicidade exata tipada; exclui inferência de chave, similaridade, normalização de valores, fórmulas, números em texto e validação de formato. | Aprovado. |
| Não intervenção | O avaliador não preenche, gera, corrige, deduplica, apaga, converte, normaliza, move ou reordena identificadores. | Aprovado. |
| Golden dataset | `GD-QLT-IDMISS-015-001`, agregado e sem identificadores, SHA-256 `f40384ef5e0c8b98d4cf7d23dfd8f8a8f5bc039c66b3051297a316274b4408b1`. | Aprovado. |
| Calibração | `CAL-QLT-IDMISS-015-001`: 3 TP, 0 FP, 0 FN em seis cenários, incluindo severidades, ausência de sinal, cabeçalho não elegível e base insuficiente. | Aprovado para draft. |
| Validação humana | Todo finding emite pergunta humana não bloqueante; o vocabulário do cabeçalho não é tratado como prova de chave única. | Aprovado. |

## Limites persistentes

Esta decisão não autoriza validar formato de CPF, CNPJ, matrículas, códigos internos ou outros identificadores; não autoriza chaves compostas, correspondência aproximada, consulta externa, inferência de chave ou qualquer transformação automática. As métricas cobrem somente o golden dataset agregado e não representam taxa de acerto operacional.

> A inclusão nesta allowlist torna a regra executável somente no perfil draft. Qualquer ampliação de vocabulário, normalização, formato, sinal, escopo ou ambiente exige nova decisão humana, novas evidências e novo gate.
