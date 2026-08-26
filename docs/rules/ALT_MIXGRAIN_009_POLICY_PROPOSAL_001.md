# ALT-MIXGRAIN-009 — Proposta A de Política 001

## Escopo proposto

Após autorização explícita de Chris para futura implementação draft, a `ALT-MIXGRAIN-009` poderá somente consolidar um **sinal já produzido por fonte independente, autorizada, opaca e agregada** de que há risco de mistura de granularidades a revisar. O resultado permitido será apenas uma solicitação conceptual de validação humana. A regra não poderá afirmar entidade, evento, chave, fato, dimensão, relacionamento, medida ou erro de negócio.

Ela não poderá inferir granularidade a partir de valores, cabeçalhos, fórmulas, formato, dados de workbook, relações, frequência, pares, posições ou conteúdo privado. Ela não poderá calcular, comparar, escolher, combinar ou separar grãos, tabelas, eventos, entidades, chaves, fatos, dimensões, medidas, unidades, populações, períodos, filtros ou agregações. Também não poderá gerar DAX, Power Query/M ou editar, excluir, reter ou exportar dados.

## Condição, supressão e privacidade

Uma eventual emissão somente será elegível com ao menos um sinal independente e agregado, contrato válido, ausência de sensibilidade e nenhuma confirmação humana prévia de granularidade única. Ausência de sinal, sinal sem autorização, confirmação humana, detalhes além de uma contagem ou flag agregada, dados sensíveis, conflito estrutural, erro contratual ou lacuna de pré-condição devem suprimir o finding de modo fail-closed. O perfil só poderá transportar contagens e flags agregadas; valores, exemplos, fórmulas, cabeçalhos, títulos, IDs, posições, pares e frequências individuais são proibidos.

## Estado de autorização

Esta Proposta A é documental e não executável sob `PROPOSAL-A-APPROVAL-DELEGATION-001`. Ela não autoriza perfil, classificador, registro, contrato, pipeline, allowlist, teste executável, golden, calibração ou produção. **Qualquer código executável requer uma autorização nova e explícita de Chris.**
