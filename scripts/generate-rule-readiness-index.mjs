import { mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "artifacts/catalogs/official-rule-blueprint-95.json");
const outputPath = resolve(root, "artifacts/catalogs/rule-implementation-readiness-v1.json");
const source = JSON.parse(await readFile(sourcePath, "utf8"));
const baseline = new Set(["QLT-NULL-001", "QLT-DUP-002", "QLT-EMPTYCOL-003", "QLT-EMPTYROW-004", "QLT-MIXTYPE-005", "QLT-BADDATE-006"]);
const executableDraft = new Set(["QLT-NUMTEXT-007"]);

const rules = source.rules.map(rule => {
  const localReadiness = baseline.has(rule.rule_id)
    ? "baseline_reference"
    : executableDraft.has(rule.rule_id)
      ? "executable_draft"
      : rule.implementation_status === "reference_implemented_draft"
        ? "reference_catalog_draft"
        : "intake_required";

  return {
    rule_id: rule.rule_id,
    title: rule.title,
    category: rule.category,
    priority: rule.priority,
    stage: rule.stage,
    scope: rule.scope,
    depends_on: rule.depends_on,
    primary_output: rule.primary_output,
    source_implementation_status: rule.implementation_status,
    local_readiness: localReadiness,
    executable: localReadiness === "executable_draft",
    missing_before_execution: localReadiness === "intake_required"
      ? ["condition", "exclusions", "evidence", "severity", "confidence", "questions", "tests", "golden_dataset", "authorization_gate"]
      : [],
  };
});

const payload = {
  readiness_id: "PM-MVP-PBI-RULE-READINESS-001",
  readiness_version: "1.0.0",
  source_blueprint: { blueprint_id: source.blueprint_id, schema_version: source.schema_version, target_count: source.target_count },
  policy: "A regra só pode ser executada quando local_readiness for executable_draft e houver gate de implementação registrado.",
  counts: Object.fromEntries(["baseline_reference", "executable_draft", "reference_catalog_draft", "intake_required"].map(status => [status, rules.filter(rule => rule.local_readiness === status).length])),
  rules,
};

await mkdir(resolve(root, "artifacts/catalogs"), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
console.log(`Índice de prontidão gerado com ${rules.length} regras em ${outputPath}.`);
