# Template de Intake para Calibração Produtiva — 001

**Estado:** template vazio e não executável. **Uso:** somente após autorização explícita de Chris. **Produção:** bloqueada.

## Registro de autorização

| Campo | Estado atual |
|---|---|
| Identificador de autorização | Não preenchido |
| Responsável pela origem | Não preenchido |
| Finalidade de processamento | Não preenchido |
| Decisão de uso | Nenhum conjunto está autorizado neste template |

## Origem e privacidade

Antes de qualquer ingestão, o responsável deverá registrar a origem autorizada, a base de tratamento aplicável, o owner responsável, a classificação de PII, o método verificável de desidentificação, o inventário de transformações e a evidência de que nenhum dado cru será copiado para logs, golden datasets, diagnósticos ou artefatos de teste. O conjunto deverá ser mínimo, temporário e owner-scoped.

## Rótulos e desenho de avaliação

Cada caso deverá ter rótulo humano verificável, versão de taxonomia, categoria, regra avaliada, severidade, decisão humana bloqueante esperada e marcador de exceção. A avaliação deve registrar TP, FP e FN por regra, categoria, severidade e estrato; também deve relatar cobertura, tamanho amostral, regras sem dados e discordâncias humanas. Não há limiar produtivo pré-aprovado neste template.

## Retenção e descarte

O intake deverá declarar prazo de retenção, local seguro, responsável, trilha de auditoria sanitizada, critério de descarte e resultado de exclusão física quando e somente quando a operação suportada estiver disponível. A remoção de referência não deverá ser declarada como exclusão física.

## Critérios de aceite para submissão de gate

Um gate posterior poderá ser solicitado somente se todos os campos acima estiverem preenchidos, os dados estiverem desidentificados e autorizados, os rótulos forem revisados, as métricas forem calculadas sem conteúdo cru em logs e os bloqueios de E2E, exclusão física e linhagem canônica estiverem resolvidos ou formalmente aceitos. O preenchimento do template não autoriza executar calibragem, alterar regras ou promover ambiente.
