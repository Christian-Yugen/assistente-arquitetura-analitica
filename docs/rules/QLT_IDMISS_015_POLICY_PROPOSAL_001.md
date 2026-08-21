# QLT-IDMISS-015 — Política proposta 001

**Estado:** não executável; aguarda autorização explícita de Chris.  
**Versão pretendida:** `0.1.0-provisional.1`.  
**Escopo:** uma coluna por avaliação.  
**Fonte recuperada:** o blueprint oficial define a detecção de nulos, duplicidades ou formatos inválidos em identificadores, com prioridade P0, escopo por coluna, dependência de profiling e saída `finding`. O Plano Mestre exige validação humana para hipóteses. Não foram recuperados formatos, dicionário de identificadores, limiares ou evidências específicas.

## Proposta A — ausência e duplicidade exata em vocabulário fechado

Esta proposta não tenta inferir chaves de negócio, nem validar formato de CPF, CNPJ, códigos internos ou qualquer outro identificador. Ela só avalia colunas cujo cabeçalho, tratado transitoriamente, corresponde exatamente a um vocabulário português fechado: `id`, `codigo`, `cod`, `chave`, `matricula`, `cpf`, `cnpj`, `numero` ou `num`. Em cada coluna elegível com pelo menos 10 células observadas, a regra conta ausências e repetição exata de valores físicos não ausentes, sem reter nem emitir qualquer identificador.

| Elemento | Política proposta |
|---|---|
| Elegibilidade | Cabeçalho normalizado por NFKC, `casefold`, remoção de acentos e colapso de espaços igual a um dos nove termos autorizados; base de pelo menos 10 células observadas. |
| Ausência | Conta `None`, texto que se reduz a vazio após `strip` e `NaN` numérico, pelos mesmos critérios privados da QLT-NULL-001. |
| Duplicidade | Conta somente valores físicos não ausentes com impressão digital transitória exata e tipada. Para texto, aplica somente NFKC; não remove espaços e não altera caixa. Para números finitos, datas e outros tipos suportados, preserva o tipo na comparação. |
| Condição | Pelo menos uma ausência ou pelo menos uma ocorrência duplicada em coluna elegível. |
| Evidência | Contagem observada, contagem ausente, contagem não ausente, grupos duplicados, ocorrências duplicadas e razões agregadas; sem cabeçalho, valor, hash, posição, exemplo, fórmula ou título de aba. |
| Severidade | Baixa até 5%; média acima de 5% até 20%; alta acima de 20% para a maior razão entre ausência e duplicidade. |
| Confiança | Moderada: a medição é determinística, mas o vocabulário de cabeçalho não prova que uma coluna seja chave única de negócio. |
| Pergunta humana | Em todo finding, solicitar confirmação genérica de que o campo representa um identificador que deve ser completo e único, e perguntar se há exceções de negócio. |
| Intervenção | Não preencher, gerar, corrigir, deduplicar, apagar, converter, normalizar, mover ou reordenar identificadores. |

## Exclusões obrigatórias

Esta proposta exclui cabeçalhos fora do vocabulário fechado, inferência de chave candidata, chaves compostas, unicidade entre colunas, correspondência aproximada, remoção de espaços ou casefold de valores, fórmulas, números em texto tratados como número, valores não finitos na comparação de duplicidade e validação de formato. Em particular, **não há finding de “formato inválido”** nesta versão: CPF, CNPJ, matrículas, números de pedido e códigos internos exigem especificações próprias e aprovadas.

> Um finding identifica ausência ou repetição exata em uma coluna potencialmente identificadora. Ele não confirma que o campo é uma chave de negócio, não prova fraude e não autoriza qualquer correção automática.

## Evidências exigidas antes da ativação draft

Após autorização, a implementação deverá oferecer perfil imutável agregado, impressão digital transitória não serializada, testes positivos, negativos, limítrofes, de privacidade e de integração, golden dataset sem identificadores brutos, manifesto SHA-256, relatório reprodutível de TP/FP/FN, gate individual de calibração e prova documental. A produção permanece bloqueada mesmo após eventual ativação draft.
