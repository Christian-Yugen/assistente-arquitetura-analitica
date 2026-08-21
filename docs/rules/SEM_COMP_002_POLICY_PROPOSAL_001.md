# SEM-COMP-002 — Política Proposta 001

**Estado:** não executável; aguarda aprovação específica de Chris.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.  
**Perfil de execução pretendido:** somente draft, se e quando todos os gates forem aprovados.

## Proposta A — `competence_date_candidate` por cabeçalho fechado e data integralmente reconhecida

Esta proposta limita a classificação à hipótese de que uma coluna represente uma data de competência. Ela somente poderá emitir `semantic_type: "competence_date_candidate"` quando houver, simultaneamente, um cabeçalho elegível no vocabulário fechado e os sinais agregados que já sustentariam a classificação `date_generic`. A regra não interpreta o significado de valores, não infere competências mensais por valores como `2026-08`, não converte datas e não decide o período contábil ou fiscal aplicável.

| Elemento | Política proposta |
|---|---|
| Vocabulário fechado | Após normalização transitória NFKC, remoção de acentos, `casefold` e compactação de espaços: `competencia`, `data competencia`, `data de competencia`. |
| Pré-condição temporal | Pelo menos 10 observações não ausentes; todas devem ser datas físicas ou textos estritamente reconhecidos pela SEM-DATE-001 (`AAAA-MM-DD`, `DD-MM-AAAA` ou `DD/MM/AAAA`). |
| Controle de fórmula | A coluna não pode conter fórmulas. A origem de uma fórmula não é evidência suficiente de competência. |
| Condição | `header_eligible = true`, `non_missing_count >= 10`, `recognized_date_ratio = 1.0` e `formula_count = 0`. |
| Saída | `competence_date_candidate`, confiança `0.85`, evidências agregadas e pergunta humana bloqueante. |
| Evidência permitida | Booleano de elegibilidade do cabeçalho, contagens agregadas de observações, datas reconhecidas e fórmulas, razão de reconhecimento e identificadores internos de entidade. |
| Intervenção | Nenhuma. A regra não corrige, converte, preenche, altera timezone, deriva mês, cria calendário, reordena ou persiste conteúdo de planilha. |

## Precedência e coexistência

A SEM-COMP-002 é uma especialização **candidata** da SEM-DATE-001. Quando sua condição estiver satisfeita, a SEM-DATE-001 pode continuar emitindo `date_generic`; a SEM-COMP-002 adiciona uma hipótese mais específica, sem suprimir, substituir ou promover automaticamente a classificação genérica. A confirmação humana bloqueante resolve a semântica de negócio antes de qualquer decisão de modelagem.

> `competence_date_candidate` não afirma que a coluna representa competência contábil, fiscal, trabalhista ou operacional. A classificação limita-se a registrar uma hipótese sustentada por um rótulo fechado e por datas integralmente reconhecidas.

## Exclusões obrigatórias

A proposta não classifica cabeçalhos como `periodo`, `referencia`, `mês`, `mes`, `data`, `competency`, `competence`, `competência financeira` ou qualquer sinônimo não listado. Também exclui cobertura temporal parcial, menos de 10 observações, valores não reconhecidos, números seriais de Excel, períodos sem dia (`AAAA-MM`), timestamps textuais, horas isoladas, booleanos, números em texto, formatos de célula, formatação visual, inferência por posição, título de aba, domínio, frequência, magnitude ou amostras de valores.

O profiler poderá avaliar o cabeçalho apenas transitoriamente para derivar `header_eligible`; não poderá persistir, serializar ou projetar o texto do cabeçalho. Valores de célula devem ser processados somente pelos sinais agregados reutilizados da SEM-DATE-001. O mascaramento preexistente de cabeçalhos e títulos de abas permanece controle independente e obrigatório.

## Evidências exigidas antes de qualquer ativação draft

Após uma aprovação explícita desta proposta, a implementação deverá produzir perfil imutável agregado, classificador determinístico, registro no catálogo, integração protegida pela allowlist, testes unitários positivos, negativos, limítrofes, de privacidade, de precedência, de contrato e de pipeline. Também deverá incluir golden dataset sintético sem dados pessoais, SHA-256, avaliador reprodutível de TP/FP/FN e gate individual de calibração. A produção continuará bloqueada.
