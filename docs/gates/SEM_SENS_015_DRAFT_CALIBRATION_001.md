## Decisão

A SEM-SENS-015 está autorizada **exclusivamente no perfil draft** após a Proposta A e o Gate de Reconstrução 001 aprovados por Chris. A autorização não promove a regra para produção nem reduz os controles de mascaramento existentes.

## Artefato de calibração

| Campo | Registro |
|---|---|
| Dataset golden | `GD-SEM-SENS-015-001` |
| Arquivo | `artifacts/golden/sem-sens-draft-golden-v1.json` |
| SHA-256 | `4f03bcde5fbdf9a2c8e634d0e05688cb7ae30c871840ef473acc6c156bb72c9e` |
| Avaliador | `engine/calibration/evaluate_sem_sens_draft_golden.py` |
| Resultado | 3 TP, 0 FP, 0 FN |
| Perfil de execução | `executable_draft` |

## Controles preservados

A regra usa somente o vocabulário fechado `cpf`, `cnpj`, `email`, `e-mail`, `nome`, `telefone`, `celular`, `endereco` e `endereço`, mais a contagem agregada de pelo menos uma observação não ausente. O classificador não inspeciona nem retém valores, cabeçalhos, títulos de abas, posições, hashes ou identificadores. A saída segregada é `sensitivity: personal_data_candidate`, com confiança `0.90`, evidências agregadas e pergunta humana bloqueante. O mascaramento existente continua como controle independente. A produção permanece bloqueada; qualquer ampliação exige nova proposta, aprovação, calibração e gate.
