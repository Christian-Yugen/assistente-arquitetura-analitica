# SEM-SENS-015 — Proposta de Política 001

**Regra:** `SEM-SENS-015` — Sensibilidade e dado pessoal.  
**Estado:** proposta não executável; execução bloqueada.  
**Escopo oficial recuperado:** regra P0 por coluna, na etapa `semantic_typing`, dependente de qualidade e com saída `sensitivity`.

## Lacuna oficial e princípio de minimização

O blueprint oficial determina a classificação de sensibilidade e dado pessoal por evidências convergentes, mas não define condição, vocabulário, exclusões, confiança, evidência, pergunta, testes ou calibração. A Proposta A evita qualquer inspeção, retenção, correspondência ou reidentificação dos valores de uma coluna. Ela usa somente um cabeçalho fechado e a contagem agregada de observações já produzida no perfil privado de identificador. O mecanismo de mascaramento existente continua independente e não poderá ser condicionado, substituído ou enfraquecido por esta regra.

## Proposta A — dado pessoal candidato

Uma coluna será classificada como `personal_data_candidate` no campo canônico `sensitivity` somente quando o cabeçalho normalizado pertencer ao vocabulário fechado `cpf`, `cnpj`, `email`, `e-mail`, `nome`, `telefone`, `celular`, `endereco` ou `endereço` e houver pelo menos uma observação não ausente na coluna. O cabeçalho será normalizado transitoriamente por NFKC, `casefold`, remoção de acentos e colapso de espaços; a presença será representada apenas por contagem agregada. Não haverá leitura semântica de valores, formatos, fórmulas, nomes de abas, posições, identificadores, hashes, domínios de e-mail ou padrões de documentos.

A hipótese terá confiança inicial de **0,90** e incluirá a pergunta humana bloqueante: **“Esta coluna contém dado pessoal ou dado identificável que deve permanecer mascarado e receber tratamento restrito na modelagem?”** A saída não representa decisão jurídica, consentimento, base legal, classificação definitiva de dado sensível ou autorização de uso.

| Elemento | Política proposta |
|---|---|
| Escopo | Coluna |
| Evidência de cabeçalho | Vocabulário fechado de identificadores pessoais |
| Evidência de presença | Ao menos uma observação não ausente, reduzida a contagem |
| Inspeção de valores | Proibida |
| Classificação | `personal_data_candidate` no campo `sensitivity` |
| Confiança | `0.90` |
| Pergunta | Obrigatória e bloqueante |
| Mascaramento existente | Independente, preservado e não condicionado à regra |

## Exclusões e privacidade

Ficam excluídos cabeçalhos fora do vocabulário fechado, colunas sem observação não ausente e inferências baseadas em conteúdo. Os termos `cliente`, `usuario`, `usuário`, `contato`, `documento`, `codigo`, `código`, `id` e `matricula` permanecem fora do vocabulário por serem insuficientes para classificar dado pessoal sem inspecionar valores. A regra não exibirá, armazenará, comparará ou derivará CPF, CNPJ, telefone, e-mail, nome, endereço ou quaisquer outros valores.

## Alternativa B — reconhecer padrões de valor

Uma alternativa seria detectar formatos de CPF, CNPJ, telefone ou e-mail nos valores. Embora amplie a cobertura, ela elevaria a superfície de processamento de dados pessoais e exigiria especificação própria de minimização, limites de retenção, testes de segurança e governança adicional. A Proposta A privilegia sinal de esquema, isolamento e controle humano; qualquer reconhecimento baseado em valores exige novo intake, política, aprovação explícita, calibração e gate.

## Condição de avanço

Esta proposta não autoriza implementação. O avanço exige aprovação explícita de Chris para a Proposta A, seguida de gate de reconstrução, perfil privado, classificador determinístico, registro, versão de contrato, integração canônica, testes positivos/negativos/limítrofes, golden dataset sem valores pessoais, calibração reprodutível, gate individual e ativação exclusivamente em draft. Produção permanece bloqueada.

## Referências internas

1. `artifacts/catalogs/official-rule-blueprint-95.json`, sequência 30, `SEM-SENS-015`.
2. `artifacts/intake/SEM-SENS-015.json`, lacunas e pré-condições recuperadas.
3. `engine/profiling/semantic_identifier.py`, sinal transitório de cabeçalho sensível e contagens agregadas.
4. `engine/profiling/workbook.py`, mecanismo existente de mascaramento por cabeçalho.
