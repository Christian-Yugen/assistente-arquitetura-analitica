# Reconstrução Governada do Contrato — CONTRACT-RECONSTRUCTION-001

## Decisão

O artefato original `diagnosis.schema.json` e seus modelos Pydantic correspondentes não foram localizados no conjunto de fontes compartilhadas. A fonte primária disponível é o documento **Contrato JSON Oficial do Diagnóstico — Fase 2 v1.0**, que descreve contrato raiz, campos, tipos, enumerações, validações estruturais e validações semânticas.

> **Decisão de governança:** reconstruir uma nova representação canônica operacional a partir do documento aprovado, com identificação, versão e linhagem próprias. O novo artefato não será apresentado como uma cópia do JSON original indisponível.

| Campo | Valor |
|---|---|
| Gate | `CONTRACT-RECONSTRUCTION-001` |
| Fonte primária | `Contrato_JSON_Oficial_Diagnostico_Fase2_v1.0.docx` |
| Artefato resultante | `artifacts/contracts/PM-MVP-PBI-CON-001/diagnosis.schema.json` |
| Versão inicial | `1.0.0-reconstructed.1` |
| Estado inicial | `draft_reconstructed` |
| Linguagem de validação estrutural | JSON Schema Draft 2020-12 |
| Linguagem de validação semântica | Pydantic |
| Promoção | Bloqueada até validação de exemplos e aprovação formal do gate |

## Regras de reconstrução

Cada propriedade reconstruída deve registrar a seção do DOCX que a fundamenta. Quando o documento especificar somente o nome e o tipo de uma estrutura aninhada, sem detalhar todos os seus campos, o schema deve aceitar o bloco como objeto provisório e registrar a lacuna; não deve inventar uma taxonomia adicional de negócio.

Valores de execução, retenção, arquivo, consentimento e projeto devem ser recebidos por metadados de entrada ou omitidos apenas quando o contrato permitir resultado parcial. O executor não pode criar identificadores, nomes de projeto, versões de termos, hashes, permissões, datas de retenção ou fatos de negócio arbitrários para aparentar completude.

## Critérios do gate

O gate pode ser aprovado somente se o schema reconstruído cobrir os blocos raiz, campos obrigatórios, enumerações, formatos e limites explicitamente descritos; os modelos Pydantic implementarem as validações cruzadas documentadas; os exemplos mínimo, completo e de erro forem validados estrutural e semanticamente; e todas as lacunas forem registradas. A aprovação deixa o contrato apto para uso operacional no MVP, mas não apaga a origem reconstruída nem elimina futura comparação com um artefato original que venha a ser recuperado.
