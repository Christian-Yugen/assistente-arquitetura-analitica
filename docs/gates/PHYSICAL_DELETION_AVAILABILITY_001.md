# Disponibilidade de Exclusão Física — 001

**Estado:** bloqueio confirmado; não autoriza produção. **Escopo:** objetos privados de workbook tratados pelo perfil draft.

## Evidência técnica

A camada `server/storage.ts` expõe somente `storagePut`, `storageGet` e `storageGetSignedUrl`. Ela usa presign de `PUT` e de `GET`; não expõe helper, endpoint ou operação de `DELETE`. A diretriz de armazenamento da plataforma determina que a remoção da chave do banco e das referências de interface é o comportamento disponível e proíbe implementar helper de remoção do objeto subjacente sem suporte da camada.

## Controle compensatório vigente

Após a análise, o fluxo draft remove a referência privada do banco e mantém somente metadados mínimos owner-scoped e sanitizados. Esse controle reduz a alcançabilidade pelo aplicativo, mas **não comprova exclusão física do objeto**. A exceção de retenção vigente e o Gate MVP permanecem aplicáveis.

## Decisão de gate

Produção permanece bloqueada até que uma operação de exclusão suportada seja disponibilizada pela camada de armazenamento e seja coberta por teste owner-scoped, falhas tratadas, auditoria sanitizada e gate individual. Este documento não adiciona endpoint, não chama armazenamento, não tenta deleção e não altera a retenção atual.

> Não é permitido simular exclusão física, declarar o objeto removido ou promover o ambiente com base apenas na remoção da referência no banco.
