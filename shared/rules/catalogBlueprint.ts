export const CATALOG_BLUEPRINT_ID = "PM-MVP-PBI-CATALOG-95";
export const CATALOG_BLUEPRINT_VERSION = "1.0.0";

export const RULE_CATEGORIES = [
  { code: "QLT", label: "Qualidade", total: 15 },
  { code: "SEM", label: "Tipagem semântica", total: 15 },
  { code: "FDM", label: "Fato e dimensão", total: 20 },
  { code: "REL", label: "Relacionamentos", total: 10 },
  { code: "MET", label: "Métricas", total: 15 },
  { code: "ALT", label: "Alertas", total: 10 },
  { code: "GRN", label: "Granularidade", total: 10 },
] as const;

export type RuleCategoryCode = (typeof RULE_CATEGORIES)[number]["code"];
export type RuleLifecycle = "baseline_draft" | "authorized_to_specify" | "reserved_definition";
export type DefinitionStatus = "baseline_reference" | "not_specified";

export type RuleDefinitionTemplate = {
  specificationStatus: DefinitionStatus;
  objective: string | null;
  scope: "column" | "sheet" | "workbook" | "model" | null;
  inputs: string[];
  condition: null;
  exclusions: string[];
  evidenceTemplates: string[];
  severityPolicy: null;
  confidencePolicy: null;
  outcomes: string[];
  questions: string[];
  recommendation: null;
  suppression: string[];
  precedence: {
    executesAfterRuleIds: string[];
    conflictsWithRuleIds: string[];
    supersedesRuleIds: string[];
  };
  dependencies: {
    requiresRuleLoadedIds: string[];
    requiresRuleFiredIds: string[];
    requiresStagesCompleted: string[];
    requiresContextPaths: string[];
  };
  sourceRequirementIds: string[];
  contextPaths: string[];
  tests: {
    unit: string[];
    interaction: string[];
    regression: string[];
  };
  goldenDatasetExpectation: {
    datasetIds: string[];
    expectedFindings: string[];
    expectedSeverity: string[];
    expectedQuestions: string[];
  };
};

export type RuleBlueprintSlot = {
  ruleId: string;
  category: RuleCategoryCode;
  categoryLabel: string;
  ordinal: number;
  name: string | null;
  lifecycle: RuleLifecycle;
  sourceStatus: "draft" | "not_specified";
  requiredDefinitionFields: readonly string[];
  releaseGate: string;
  definition: RuleDefinitionTemplate;
};

export type CatalogBlueprint = {
  blueprintId: string;
  blueprintVersion: string;
  diagnosisContractVersion: "1.0.0";
  status: "frozen_structure";
  slots: RuleBlueprintSlot[];
};

export const REQUIRED_RULE_DEFINITION_FIELDS = [
  "rule_id",
  "category",
  "name",
  "objective",
  "scope",
  "inputs",
  "condition",
  "exclusions",
  "evidence_templates",
  "severity_policy",
  "confidence_policy",
  "outcomes",
  "questions",
  "recommendation",
  "suppression",
  "precedence",
  "dependencies",
  "source_requirement_ids",
  "context_paths",
  "tests",
  "golden_dataset_expectation",
  "status",
] as const;

const BASELINE_RULES: Record<string, string> = {
  "QLT-001": "Alta presença de valores nulos",
  "QLT-002": "Registros totalmente duplicados",
  "QLT-003": "Colunas totalmente vazias",
  "QLT-004": "Linhas totalmente vazias",
  "QLT-005": "Tipos físicos mistos na coluna",
  "QLT-006": "Datas inválidas em coluna temporal",
};

const AUTHORIZED_RULES: Record<string, string> = {
  "QLT-007": "Valores numéricos armazenados como texto",
};

function pad(value: number) {
  return String(value).padStart(3, "0");
}

function createDefinitionTemplate(lifecycle: RuleLifecycle): RuleDefinitionTemplate {
  return {
    specificationStatus: lifecycle === "baseline_draft" ? "baseline_reference" : "not_specified",
    objective: null,
    scope: null,
    inputs: [],
    condition: null,
    exclusions: [],
    evidenceTemplates: [],
    severityPolicy: null,
    confidencePolicy: null,
    outcomes: [],
    questions: [],
    recommendation: null,
    suppression: [],
    precedence: {
      executesAfterRuleIds: [],
      conflictsWithRuleIds: [],
      supersedesRuleIds: [],
    },
    dependencies: {
      requiresRuleLoadedIds: [],
      requiresRuleFiredIds: [],
      requiresStagesCompleted: [],
      requiresContextPaths: [],
    },
    sourceRequirementIds: [],
    contextPaths: [],
    tests: {
      unit: [],
      interaction: [],
      regression: [],
    },
    goldenDatasetExpectation: {
      datasetIds: [],
      expectedFindings: [],
      expectedSeverity: [],
      expectedQuestions: [],
    },
  };
}

export function buildCatalogBlueprint(): RuleBlueprintSlot[] {
  return RULE_CATEGORIES.flatMap(category =>
    Array.from({ length: category.total }, (_, index) => {
      const ordinal = index + 1;
      const ruleId = `${category.code}-${pad(ordinal)}`;
      const baselineName = BASELINE_RULES[ruleId];
      const authorizedName = AUTHORIZED_RULES[ruleId];
      const lifecycle = baselineName
        ? "baseline_draft"
        : authorizedName
          ? "authorized_to_specify"
          : "reserved_definition";

      return {
        ruleId,
        category: category.code,
        categoryLabel: category.label,
        ordinal,
        name: baselineName ?? authorizedName ?? null,
        lifecycle,
        sourceStatus: baselineName ? "draft" : "not_specified",
        requiredDefinitionFields: REQUIRED_RULE_DEFINITION_FIELDS,
        releaseGate: baselineName
          ? "Baseline G6.5; production blocked pending calibration"
          : authorizedName
            ? "Global QLT-001-006 gate; rule-specific implementation gate required"
            : "Blueprint frozen; business policy and rule-specific authorization required",
        definition: createDefinitionTemplate(lifecycle),
      };
    }),
  );
}

export const CATALOG_BLUEPRINT: CatalogBlueprint = {
  blueprintId: CATALOG_BLUEPRINT_ID,
  blueprintVersion: CATALOG_BLUEPRINT_VERSION,
  diagnosisContractVersion: "1.0.0",
  status: "frozen_structure",
  slots: buildCatalogBlueprint(),
};

export function summarizeCatalogBlueprint(slots = CATALOG_BLUEPRINT.slots) {
  return RULE_CATEGORIES.map(category => {
    const categorySlots = slots.filter(slot => slot.category === category.code);
    const baseline = categorySlots.filter(slot => slot.lifecycle === "baseline_draft").length;
    const authorized = categorySlots.filter(slot => slot.lifecycle === "authorized_to_specify").length;

    return {
      category: category.code,
      total: categorySlots.length,
      baseline,
      authorized,
      reserved: categorySlots.length - baseline - authorized,
    };
  });
}
