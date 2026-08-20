/**
 * Importado sem alteração semântica de PM-MVP-PBI-RULE-BP-001 v1.0.0.
 * Não edite manualmente; regenere com scripts/import-official-blueprint.mjs.
 */
export const OFFICIAL_CATALOG_ID = "PM-MVP-PBI-RULE-BP-001" as const;
export const OFFICIAL_CATALOG_VERSION = "1.0.0" as const;
export const OFFICIAL_CATALOG_RULES = [
  {
    "ruleId": "QLT-NULL-001",
    "category": "quality",
    "title": "Valores nulos relevantes",
    "purpose": "Detectar ausência elevada e qualquer nulo em chave candidata.",
    "priority": "P0",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "reference_implemented_draft"
  },
  {
    "ruleId": "QLT-DUP-002",
    "category": "quality",
    "title": "Registros duplicados",
    "purpose": "Detectar linhas totalmente duplicadas.",
    "priority": "P0",
    "stage": "quality",
    "scope": "sheet",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-EMPTYCOL-003",
    "category": "quality",
    "title": "Colunas vazias",
    "purpose": "Detectar colunas sem informação útil.",
    "priority": "P1",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-EMPTYROW-004",
    "category": "quality",
    "title": "Linhas vazias",
    "purpose": "Detectar linhas totalmente vazias na região tabular.",
    "priority": "P1",
    "stage": "quality",
    "scope": "sheet",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-MIXTYPE-005",
    "category": "quality",
    "title": "Tipos mistos",
    "purpose": "Detectar coexistência incompatível de tipos.",
    "priority": "P0",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-BADDATE-006",
    "category": "quality",
    "title": "Datas inválidas",
    "purpose": "Detectar valores que não podem ser convertidos em datas.",
    "priority": "P0",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-NUMTEXT-007",
    "category": "quality",
    "title": "Números armazenados como texto",
    "purpose": "Detectar números serializados como texto.",
    "priority": "P1",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-CATVAR-008",
    "category": "quality",
    "title": "Variações de categoria",
    "purpose": "Detectar grafias potencialmente equivalentes.",
    "priority": "P1",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-WHITESPACE-009",
    "category": "quality",
    "title": "Espaços e caracteres ocultos",
    "purpose": "Detectar sujeira textual estrutural.",
    "priority": "P1",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-TOTALROW-010",
    "category": "quality",
    "title": "Linhas totalizadoras",
    "purpose": "Detectar totais e subtotais dentro da tabela.",
    "priority": "P0",
    "stage": "quality",
    "scope": "sheet",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-NEGATIVE-011",
    "category": "quality",
    "title": "Valores negativos suspeitos",
    "purpose": "Detectar sinais incompatíveis com a semântica provável.",
    "priority": "P1",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-OUTLIER-012",
    "category": "quality",
    "title": "Valores atípicos",
    "purpose": "Detectar extremos estatísticos para validação.",
    "priority": "P1",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-FORMULA-013",
    "category": "quality",
    "title": "Fórmulas inconsistentes",
    "purpose": "Detectar padrões de fórmula divergentes.",
    "priority": "P1",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-HEADERS-014",
    "category": "quality",
    "title": "Cabeçalhos inválidos",
    "purpose": "Detectar cabeçalhos ausentes, duplicados ou multinível.",
    "priority": "P0",
    "stage": "quality",
    "scope": "sheet",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "QLT-IDMISS-015",
    "category": "quality",
    "title": "Identificadores incompletos",
    "purpose": "Detectar nulos, duplicidades ou formatos inválidos em identificadores.",
    "priority": "P0",
    "stage": "quality",
    "scope": "column",
    "dependsOn": [
      "profiling"
    ],
    "primaryOutput": "finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-DATE-001",
    "category": "semantic_typing",
    "title": "Data genérica",
    "purpose": "Classificar coluna como data genérica com evidências convergentes.",
    "priority": "P0",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "reference_implemented_draft"
  },
  {
    "ruleId": "SEM-COMP-002",
    "category": "semantic_typing",
    "title": "Data de competência",
    "purpose": "Classificar coluna como data de competência com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-ID-003",
    "category": "semantic_typing",
    "title": "Identificador",
    "purpose": "Classificar coluna como identificador com evidências convergentes.",
    "priority": "P0",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-DESC-004",
    "category": "semantic_typing",
    "title": "Nome ou descrição",
    "purpose": "Classificar coluna como nome ou descrição com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-QTY-005",
    "category": "semantic_typing",
    "title": "Quantidade",
    "purpose": "Classificar coluna como quantidade com evidências convergentes.",
    "priority": "P0",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-CURR-006",
    "category": "semantic_typing",
    "title": "Valor monetário",
    "purpose": "Classificar coluna como valor monetário com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-PCT-007",
    "category": "semantic_typing",
    "title": "Percentual",
    "purpose": "Classificar coluna como percentual com evidências convergentes.",
    "priority": "P0",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-DUR-008",
    "category": "semantic_typing",
    "title": "Duração",
    "purpose": "Classificar coluna como duração com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-STATUS-009",
    "category": "semantic_typing",
    "title": "Status",
    "purpose": "Classificar coluna como status com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-CAT-010",
    "category": "semantic_typing",
    "title": "Categoria",
    "purpose": "Classificar coluna como categoria com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-LOC-011",
    "category": "semantic_typing",
    "title": "Localização",
    "purpose": "Classificar coluna como localização com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-RESP-012",
    "category": "semantic_typing",
    "title": "Responsável",
    "purpose": "Classificar coluna como responsável com evidências convergentes.",
    "priority": "P1",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-TARGET-013",
    "category": "semantic_typing",
    "title": "Meta ou previsto",
    "purpose": "Classificar coluna como meta ou previsto com evidências convergentes.",
    "priority": "P0",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-ACTUAL-014",
    "category": "semantic_typing",
    "title": "Realizado",
    "purpose": "Classificar coluna como realizado com evidências convergentes.",
    "priority": "P0",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "semantic_type",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "SEM-SENS-015",
    "category": "semantic_typing",
    "title": "Sensibilidade e dado pessoal",
    "purpose": "Classificar coluna como sensibilidade e dado pessoal com evidências convergentes.",
    "priority": "P0",
    "stage": "semantic_typing",
    "scope": "column",
    "dependsOn": [
      "quality"
    ],
    "primaryOutput": "sensitivity",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-COMP-001",
    "category": "grain",
    "title": "Chave composta",
    "purpose": "Inferir ou validar chave composta.",
    "priority": "P0",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "reference_implemented_draft"
  },
  {
    "ruleId": "GRN-EXPL-002",
    "category": "grain",
    "title": "Chave explícita",
    "purpose": "Inferir ou validar chave explícita.",
    "priority": "P0",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-ENTITY-003",
    "category": "grain",
    "title": "Entidade por linha",
    "purpose": "Inferir ou validar entidade por linha.",
    "priority": "P1",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-EVENT-004",
    "category": "grain",
    "title": "Evento por linha",
    "purpose": "Inferir ou validar evento por linha.",
    "priority": "P0",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-PERIOD-005",
    "category": "grain",
    "title": "Período por linha",
    "purpose": "Inferir ou validar período por linha.",
    "priority": "P0",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-SNAP-006",
    "category": "grain",
    "title": "Snapshot periódico",
    "purpose": "Inferir ou validar snapshot periódico.",
    "priority": "P1",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-ASSOC-007",
    "category": "grain",
    "title": "Associação entre entidades",
    "purpose": "Inferir ou validar associação entre entidades.",
    "priority": "P1",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-PREAGG-008",
    "category": "grain",
    "title": "Agregação prévia",
    "purpose": "Inferir ou validar agregação prévia.",
    "priority": "P1",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-INCONS-009",
    "category": "grain",
    "title": "Granularidade inconsistente",
    "purpose": "Inferir ou validar granularidade inconsistente.",
    "priority": "P0",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "GRN-DUP-010",
    "category": "grain",
    "title": "Duplicidade na granularidade",
    "purpose": "Inferir ou validar duplicidade na granularidade.",
    "priority": "P0",
    "stage": "grain_inference",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing"
    ],
    "primaryOutput": "grain",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-FACTPER-001",
    "category": "fact_dimension",
    "title": "Fato periódica",
    "purpose": "Classificar ou propor fato periódica.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "reference_implemented_draft"
  },
  {
    "ruleId": "MDL-FACTTXN-002",
    "category": "fact_dimension",
    "title": "Fato transacional",
    "purpose": "Classificar ou propor fato transacional.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-FACTACC-003",
    "category": "fact_dimension",
    "title": "Snapshot acumulado",
    "purpose": "Classificar ou propor snapshot acumulado.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-DIMSTD-004",
    "category": "fact_dimension",
    "title": "Dimensão cadastral",
    "purpose": "Classificar ou propor dimensão cadastral.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-DIMCONF-005",
    "category": "fact_dimension",
    "title": "Dimensão compartilhada",
    "purpose": "Classificar ou propor dimensão compartilhada.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-DIMCAL-006",
    "category": "fact_dimension",
    "title": "Dimensão calendário",
    "purpose": "Classificar ou propor dimensão calendário.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-DIMROLE-007",
    "category": "fact_dimension",
    "title": "Dimensão de função",
    "purpose": "Classificar ou propor dimensão de função.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-DIMDEG-008",
    "category": "fact_dimension",
    "title": "Dimensão degenerada",
    "purpose": "Classificar ou propor dimensão degenerada.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-BRIDGE-009",
    "category": "fact_dimension",
    "title": "Tabela ponte",
    "purpose": "Classificar ou propor tabela ponte.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-AUX-010",
    "category": "fact_dimension",
    "title": "Tabela auxiliar",
    "purpose": "Classificar ou propor tabela auxiliar.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-PARAM-011",
    "category": "fact_dimension",
    "title": "Tabela parâmetro como auxiliar",
    "purpose": "Classificar ou propor tabela parâmetro como auxiliar.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-FLAT-012",
    "category": "fact_dimension",
    "title": "Tabela desnormalizada",
    "purpose": "Classificar ou propor tabela desnormalizada.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-MIXED-013",
    "category": "fact_dimension",
    "title": "Tabela mista",
    "purpose": "Classificar ou propor tabela mista.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-ATTRREP-014",
    "category": "fact_dimension",
    "title": "Atributos repetidos",
    "purpose": "Classificar ou propor atributos repetidos.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-MEASURE-015",
    "category": "fact_dimension",
    "title": "Medidas armazenadas",
    "purpose": "Classificar ou propor medidas armazenadas.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-DIMEXTRACT-016",
    "category": "fact_dimension",
    "title": "Dimensão extraível da fato",
    "purpose": "Classificar ou propor dimensão extraível da fato.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-DIMMISS-017",
    "category": "fact_dimension",
    "title": "Dimensão ausente",
    "purpose": "Classificar ou propor dimensão ausente.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-FACTNOMEAS-018",
    "category": "fact_dimension",
    "title": "Fato sem medidas",
    "purpose": "Classificar ou propor fato sem medidas.",
    "priority": "P1",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-FACTNOGRAIN-019",
    "category": "fact_dimension",
    "title": "Fato sem granularidade",
    "purpose": "Classificar ou propor fato sem granularidade.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MDL-UNDEFINED-020",
    "category": "fact_dimension",
    "title": "Classificação indefinida",
    "purpose": "Classificar ou propor classificação indefinida.",
    "priority": "P0",
    "stage": "table_classification",
    "scope": "sheet",
    "dependsOn": [
      "grain"
    ],
    "primaryOutput": "classification_or_table",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-ONEMANY-001",
    "category": "relationship",
    "title": "Relacionamento um-para-muitos",
    "purpose": "Detectar ou recomendar relacionamento um-para-muitos.",
    "priority": "P0",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "reference_implemented_draft"
  },
  {
    "ruleId": "REL-NONUNIQ-002",
    "category": "relationship",
    "title": "Chave não única no lado 1",
    "purpose": "Detectar ou recomendar chave não única no lado 1.",
    "priority": "P0",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-ORPHAN-003",
    "category": "relationship",
    "title": "Registros órfãos",
    "purpose": "Detectar ou recomendar registros órfãos.",
    "priority": "P1",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-MANYMANY-004",
    "category": "relationship",
    "title": "Muitos-para-muitos",
    "purpose": "Detectar ou recomendar muitos-para-muitos.",
    "priority": "P0",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-BRIDGE-005",
    "category": "relationship",
    "title": "Necessidade de ponte",
    "purpose": "Detectar ou recomendar necessidade de ponte.",
    "priority": "P1",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-FACTFACT-006",
    "category": "relationship",
    "title": "Relacionamento direto entre fatos",
    "purpose": "Detectar ou recomendar relacionamento direto entre fatos.",
    "priority": "P0",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-AMBIG-007",
    "category": "relationship",
    "title": "Caminhos ambíguos",
    "purpose": "Detectar ou recomendar caminhos ambíguos.",
    "priority": "P0",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-BIDIR-008",
    "category": "relationship",
    "title": "Filtro bidirecional suspeito",
    "purpose": "Detectar ou recomendar filtro bidirecional suspeito.",
    "priority": "P0",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-COMPKEY-009",
    "category": "relationship",
    "title": "Chave composta",
    "purpose": "Detectar ou recomendar chave composta.",
    "priority": "P1",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "REL-CONFORMED-010",
    "category": "relationship",
    "title": "Dimensão compartilhada",
    "purpose": "Detectar ou recomendar dimensão compartilhada.",
    "priority": "P1",
    "stage": "relationship_inference",
    "scope": "sheet_pair",
    "dependsOn": [
      "table_classification"
    ],
    "primaryOutput": "relationship_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-COMPL-001",
    "category": "metric",
    "title": "Percentual de conclusão",
    "purpose": "Sugerir ou validar percentual de conclusão.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "reference_implemented_draft"
  },
  {
    "ruleId": "MET-SUM-002",
    "category": "metric",
    "title": "Soma",
    "purpose": "Sugerir ou validar soma.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-COUNT-003",
    "category": "metric",
    "title": "Contagem",
    "purpose": "Sugerir ou validar contagem.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-DCOUNT-004",
    "category": "metric",
    "title": "Contagem distinta",
    "purpose": "Sugerir ou validar contagem distinta.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-AVG-005",
    "category": "metric",
    "title": "Média",
    "purpose": "Sugerir ou validar média.",
    "priority": "P1",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-MINMAX-006",
    "category": "metric",
    "title": "Mínimo e máximo",
    "purpose": "Sugerir ou validar mínimo e máximo.",
    "priority": "P1",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-RATE-007",
    "category": "metric",
    "title": "Taxa",
    "purpose": "Sugerir ou validar taxa.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-ABSDELTA-008",
    "category": "metric",
    "title": "Variação absoluta",
    "purpose": "Sugerir ou validar variação absoluta.",
    "priority": "P1",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-PCTDELTA-009",
    "category": "metric",
    "title": "Variação percentual",
    "purpose": "Sugerir ou validar variação percentual.",
    "priority": "P1",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-RUNNING-010",
    "category": "metric",
    "title": "Acumulado",
    "purpose": "Sugerir ou validar acumulado.",
    "priority": "P1",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-WAVG-011",
    "category": "metric",
    "title": "Média ponderada",
    "purpose": "Sugerir ou validar média ponderada.",
    "priority": "P1",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-SEMIADD-012",
    "category": "metric",
    "title": "Medida semiaditiva",
    "purpose": "Sugerir ou validar medida semiaditiva.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-DOMAIN-013",
    "category": "metric",
    "title": "Métrica de domínio",
    "purpose": "Sugerir ou validar métrica de domínio.",
    "priority": "P1",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-IMPOSS-014",
    "category": "metric",
    "title": "Métrica insuficiente",
    "purpose": "Sugerir ou validar métrica insuficiente.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "MET-DAX-015",
    "category": "metric",
    "title": "DAX derivado da fórmula conceitual",
    "purpose": "Sugerir ou validar dax derivado da fórmula conceitual.",
    "priority": "P0",
    "stage": "metric_suggestion",
    "scope": "sheet",
    "dependsOn": [
      "semantic_typing",
      "grain_inference"
    ],
    "primaryOutput": "metric_or_finding",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-SENS-001",
    "category": "alert",
    "title": "Dado pessoal ou sensível",
    "purpose": "Consolidar alerta de dado pessoal ou sensível.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "column",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "reference_implemented_draft"
  },
  {
    "ruleId": "ALT-QUALITY-002",
    "category": "alert",
    "title": "Risco crítico de qualidade",
    "purpose": "Consolidar alerta de risco crítico de qualidade.",
    "priority": "P1",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-GRAIN-003",
    "category": "alert",
    "title": "Granularidade indefinida",
    "purpose": "Consolidar alerta de granularidade indefinida.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-KEY-004",
    "category": "alert",
    "title": "Chave inválida",
    "purpose": "Consolidar alerta de chave inválida.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-AMBIG-005",
    "category": "alert",
    "title": "Relacionamento ambíguo",
    "purpose": "Consolidar alerta de relacionamento ambíguo.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-METRIC-006",
    "category": "alert",
    "title": "Métrica potencialmente enganosa",
    "purpose": "Consolidar alerta de métrica potencialmente enganosa.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-SUMPCT-007",
    "category": "alert",
    "title": "Soma de percentuais",
    "purpose": "Consolidar alerta de soma de percentuais.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-AVGAVG-008",
    "category": "alert",
    "title": "Média de médias",
    "purpose": "Consolidar alerta de média de médias.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-MIXGRAIN-009",
    "category": "alert",
    "title": "Mistura de granularidades",
    "purpose": "Consolidar alerta de mistura de granularidades.",
    "priority": "P0",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  },
  {
    "ruleId": "ALT-LOWCONF-010",
    "category": "alert",
    "title": "Baixa confiança acumulada",
    "purpose": "Consolidar alerta de baixa confiança acumulada.",
    "priority": "P1",
    "stage": "alert_consolidation",
    "scope": "model",
    "dependsOn": [
      "quality",
      "semantic_typing",
      "grain_inference",
      "table_classification",
      "relationship_inference",
      "metric_suggestion"
    ],
    "primaryOutput": "finding_or_suppression",
    "implementationStatus": "planned"
  }
] as const;
