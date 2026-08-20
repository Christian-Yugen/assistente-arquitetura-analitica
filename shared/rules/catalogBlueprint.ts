import { OFFICIAL_CATALOG_ID, OFFICIAL_CATALOG_RULES, OFFICIAL_CATALOG_VERSION } from "./officialCatalog";

export const CATALOG_BLUEPRINT_ID = OFFICIAL_CATALOG_ID;
export const CATALOG_BLUEPRINT_VERSION = OFFICIAL_CATALOG_VERSION;

export const RULE_CATEGORIES = [
  { code: "QLT", sourceCategory: "quality", label: "Qualidade", total: 15 },
  { code: "SEM", sourceCategory: "semantic_typing", label: "Tipagem semântica", total: 15 },
  { code: "GRN", sourceCategory: "grain", label: "Granularidade", total: 10 },
  { code: "MDL", sourceCategory: "fact_dimension", label: "Fato e dimensão", total: 20 },
  { code: "REL", sourceCategory: "relationship", label: "Relacionamentos", total: 10 },
  { code: "MET", sourceCategory: "metric", label: "Métricas", total: 15 },
  { code: "ALT", sourceCategory: "alert", label: "Alertas", total: 10 },
] as const;

export type RuleCategoryCode = (typeof RULE_CATEGORIES)[number]["code"];
export type RuleLifecycle =
  | "baseline_draft"
  | "authorized_to_specify"
  | "reference_catalog_draft"
  | "reserved_definition";
export type DefinitionStatus = "baseline_reference" | "not_specified";
export type OfficialImplementationStatus = (typeof OFFICIAL_CATALOG_RULES)[number]["implementationStatus"];

export type RuleDefinitionTemplate = {
  specificationStatus: DefinitionStatus;
  objective: string | null;
  scope: "column" | "sheet" | "sheet_pair" | "workbook" | "model" | null;
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
  precedence: { executesAfterRuleIds: string[]; conflictsWithRuleIds: string[]; supersedesRuleIds: string[] };
  dependencies: {
    requiresRuleLoadedIds: string[];
    requiresRuleFiredIds: string[];
    requiresStagesCompleted: string[];
    requiresContextPaths: string[];
  };
  sourceRequirementIds: string[];
  contextPaths: string[];
  tests: { unit: string[]; interaction: string[]; regression: string[] };
  goldenDatasetExpectation: { datasetIds: string[]; expectedFindings: string[]; expectedSeverity: string[]; expectedQuestions: string[] };
};

export type RuleBlueprintSlot = {
  ruleId: string;
  category: RuleCategoryCode;
  sourceCategory: string;
  categoryLabel: string;
  ordinal: number;
  name: string;
  sourcePurpose: string;
  priority: string;
  stage: string;
  primaryOutput: string;
  sourceImplementationStatus: OfficialImplementationStatus;
  lifecycle: RuleLifecycle;
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
  "rule_id", "category", "name", "objective", "scope", "inputs", "condition", "exclusions",
  "evidence_templates", "severity_policy", "confidence_policy", "outcomes", "questions", "recommendation",
  "suppression", "precedence", "dependencies", "source_requirement_ids", "context_paths", "tests",
  "golden_dataset_expectation", "status",
] as const;

const CURRENT_QUALITY_BASELINE = new Set([
  "QLT-NULL-001", "QLT-DUP-002", "QLT-EMPTYCOL-003", "QLT-EMPTYROW-004", "QLT-MIXTYPE-005", "QLT-BADDATE-006",
]);
const CURRENTLY_AUTHORIZED = new Set(["QLT-NUMTEXT-007"]);

function getRuleCategory(ruleId: string): RuleCategoryCode {
  return ruleId.slice(0, 3) as RuleCategoryCode;
}

function lifecycleFor(rule: (typeof OFFICIAL_CATALOG_RULES)[number]): RuleLifecycle {
  if (CURRENT_QUALITY_BASELINE.has(rule.ruleId)) return "baseline_draft";
  if (CURRENTLY_AUTHORIZED.has(rule.ruleId)) return "authorized_to_specify";
  if (rule.implementationStatus === "reference_implemented_draft") return "reference_catalog_draft";
  return "reserved_definition";
}

function releaseGateFor(ruleId: string, lifecycle: RuleLifecycle): string {
  if (lifecycle === "baseline_draft") return "Baseline QLT-001 a QLT-006; produção bloqueada até calibração";
  if (lifecycle === "authorized_to_specify") return "G7.4-R1; fechamento G7.5 e produção ainda bloqueados";
  if (lifecycle === "reference_catalog_draft") return `Referência de Fase 3A.1; gate de implementação local obrigatório para ${ruleId}`;
  return "Blueprint oficial congelado; especificação, testes e gate de implementação obrigatórios";
}

function createDefinitionTemplate(rule: (typeof OFFICIAL_CATALOG_RULES)[number], lifecycle: RuleLifecycle): RuleDefinitionTemplate {
  return {
    specificationStatus: lifecycle === "reference_catalog_draft" || lifecycle === "baseline_draft" ? "baseline_reference" : "not_specified",
    objective: rule.purpose,
    scope: rule.scope,
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
    precedence: { executesAfterRuleIds: [], conflictsWithRuleIds: [], supersedesRuleIds: [] },
    dependencies: {
      requiresRuleLoadedIds: [],
      requiresRuleFiredIds: [],
      requiresStagesCompleted: [...rule.dependsOn],
      requiresContextPaths: [],
    },
    sourceRequirementIds: [],
    contextPaths: [],
    tests: { unit: [], interaction: [], regression: [] },
    goldenDatasetExpectation: { datasetIds: [], expectedFindings: [], expectedSeverity: [], expectedQuestions: [] },
  };
}

export function buildCatalogBlueprint(): RuleBlueprintSlot[] {
  return OFFICIAL_CATALOG_RULES.map((rule, index) => {
    const lifecycle = lifecycleFor(rule);
    const category = getRuleCategory(rule.ruleId);
    const categoryDefinition = RULE_CATEGORIES.find(item => item.code === category);
    if (!categoryDefinition) throw new Error(`Namespace oficial não mapeado: ${rule.ruleId}`);

    return {
      ruleId: rule.ruleId,
      category,
      sourceCategory: rule.category,
      categoryLabel: categoryDefinition.label,
      ordinal: index + 1,
      name: rule.title,
      sourcePurpose: rule.purpose,
      priority: rule.priority,
      stage: rule.stage,
      primaryOutput: rule.primaryOutput,
      sourceImplementationStatus: rule.implementationStatus,
      lifecycle,
      requiredDefinitionFields: REQUIRED_RULE_DEFINITION_FIELDS,
      releaseGate: releaseGateFor(rule.ruleId, lifecycle),
      definition: createDefinitionTemplate(rule, lifecycle),
    };
  });
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
    const count = (lifecycle: RuleLifecycle) => categorySlots.filter(slot => slot.lifecycle === lifecycle).length;
    return {
      category: category.code,
      total: categorySlots.length,
      baseline: count("baseline_draft"),
      authorized: count("authorized_to_specify"),
      references: count("reference_catalog_draft"),
      reserved: count("reserved_definition"),
    };
  });
}
