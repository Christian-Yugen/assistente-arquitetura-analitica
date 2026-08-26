# ALT-AVGAVG-008 — Proposta A de Política 001

## Escopo proposto

Após autorização explícita de Chris para futura implementação draft, a `ALT-AVGAVG-008` poderá somente consolidar um **sinal já produzido por fonte independente, autorizada, opaca e agregada** de que uma média de médias exige revisão humana. O único resultado permitido será uma solicitação conceptual de validação. A regra não afirmará que uma média, métrica, decisão de negócio ou dashboard está errado.

Ela não poderá identificar médias por valores, cabeçalhos, fórmulas, formato, dados de workbook, relações, frequência, pares, posições ou conteúdo privado. Ela não poderá calcular, recomputar, ponderar, comparar, corrigir ou escolher médias, pesos, denominadores, tamanhos de grupo, medidas, campos, entidades, unidades, populações, períodos, filtros ou agregações. Também não poderá gerar DAX, Power Query/M ou editar, excluir, reter ou exportar dados.

## Condição e supressão propostas

Uma eventual emissão somente será elegível com ao menos um sinal independente e agregado, contrato válido, ausência de sensibilidade, ausência de conflito estrutural e nenhuma confirmação humana prévia de que a composição de médias é adequada. Ausência de sinal, sinal sem autorização, confirmação humana, detalhes além de uma contagem ou flag agregada, dados sensíveis, conflito estrutural, erro contratual ou lacuna de pré-condição devem suprimir o finding de modo fail-closed.

## Saída restrita e privacidade

O finding futuro será conceptual, de alta prioridade apenas para revisão, com pergunta humana bloqueante sobre população, peso, denominador, período e interpretação confirmados. Ele não escolherá nem nomeará dado, média, medida ou contexto de negócio. O perfil só poderá transportar contagens e flags agregadas; valores, exemplos, fórmulas, cabeçalhos, títulos, IDs, posições, pares e frequências individuais são proibidos. O golden deverá ser estritamente sintético e a produção continuará bloqueada.

## Estado de autorização

Esta Proposta A é documental e não executável sob `PROPOSAL-A-APPROVAL-DELEGATION-001`. Ela não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, teste executável, golden, calibração ou produção. **Qualquer código executável requer uma autorização nova e explícita de Chris.**
