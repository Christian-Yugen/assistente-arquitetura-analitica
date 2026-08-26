# Política de Upload CSV Draft — 001

**Estado:** política autorizada para implementação no perfil draft; não altera regras de modelagem, não libera produção e não reduz controles de privacidade.

## Escopo

O fluxo aceitará arquivos `.csv` como uma única aba lógica. O arquivo será tratado somente no servidor e normalizado temporariamente antes do profiler existente, sem persistir valores brutos, títulos, amostras ou conteúdo de células no diagnóstico.

| Controle | Política autorizada |
|---|---|
| Extensão | Somente `.csv`, além do suporte XLSX já existente. |
| MIME aceito | `text/csv`, `application/csv`, `application/vnd.ms-excel` ou `application/octet-stream`, sempre com extensão correspondente. |
| Tamanho | Entre 1 byte e 25 MB. |
| Codificação | UTF-8 ou UTF-8 com BOM. Qualquer outra codificação é rejeitada. |
| Delimitador | Vírgula, ponto e vírgula ou tabulação, detectado de forma determinística. |
| Estrutura | Uma única aba lógica, cabeçalho obrigatório, até 512 colunas e 250.000 registros de dados. |
| Valores | Texto que pareça fórmula permanece texto; números canônicos e datas ISO estritas podem ser tipados sem inferir formatos ambíguos. |
| Rejeição | Arquivo binário, NUL, codificação inválida, delimitador não suportado, ausência de cabeçalho, linhas com mais campos que o cabeçalho ou limites excedidos falham de forma fechada. |

## Privacidade e retenção

O CSV seguirá o mesmo owner scope, checksum, sanitização, remoção de referência privada e diagnóstico agregado do XLSX. Nenhum atalho permitirá expor conteúdo em logs, erros, banco ou interface. A remoção de referência não equivale a exclusão física; esse bloqueio produtivo permanece.

## Limites de análise

CSV não possui abas, fórmulas, formatação de moeda ou metadados de célula equivalentes ao XLSX. Portanto, regras que dependem desses sinais permanecerão conservadoras ou sem finding. O suporte CSV não altera os limiares de amostra, a allowlist de 95 regras draft, a necessidade de confirmação humana ou o bloqueio de produção.
