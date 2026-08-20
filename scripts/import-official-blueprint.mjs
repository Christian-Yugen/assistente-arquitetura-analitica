import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const [sourcePath] = process.argv.slice(2);
if (!sourcePath) {
  throw new Error("Uso: node scripts/import-official-blueprint.mjs <caminho-do-blueprint-oficial.json>");
}

const projectRoot = resolve(import.meta.dirname, "..");
const blueprint = JSON.parse(await readFile(sourcePath, "utf8"));
if (blueprint.blueprint_id !== "PM-MVP-PBI-RULE-BP-001" || blueprint.target_count !== 95 || !Array.isArray(blueprint.rules)) {
  throw new Error("A fonte não é o blueprint oficial esperado de 95 regras.");
}

const normalized = {
  ...blueprint,
  imported_from: "PM-MVP-PBI-RULE-BP-001 v1.0.0",
  imported_for: "Assistente de Arquitetura Analítica",
};
const jsonPath = resolve(projectRoot, "artifacts/catalogs/official-rule-blueprint-95.json");
await mkdir(dirname(jsonPath), { recursive: true });
await writeFile(jsonPath, `${JSON.stringify(normalized, null, 2)}\n`, "utf8");

const entries = normalized.rules.map(rule => ({
  ruleId: rule.rule_id,
  category: rule.category,
  title: rule.title,
  purpose: rule.purpose,
  priority: rule.priority,
  stage: rule.stage,
  scope: rule.scope,
  dependsOn: rule.depends_on,
  primaryOutput: rule.primary_output,
  implementationStatus: rule.implementation_status,
}));
const ts = `/**\n * Importado sem alteração semântica de PM-MVP-PBI-RULE-BP-001 v1.0.0.\n * Não edite manualmente; regenere com scripts/import-official-blueprint.mjs.\n */\nexport const OFFICIAL_CATALOG_ID = ${JSON.stringify(normalized.blueprint_id)} as const;\nexport const OFFICIAL_CATALOG_VERSION = ${JSON.stringify(normalized.schema_version)} as const;\nexport const OFFICIAL_CATALOG_RULES = ${JSON.stringify(entries, null, 2)} as const;\n`;
const tsPath = resolve(projectRoot, "shared/rules/officialCatalog.ts");
await mkdir(dirname(tsPath), { recursive: true });
await writeFile(tsPath, ts, "utf8");

console.log(`Importadas ${entries.length} regras oficiais para ${jsonPath} e ${tsPath}.`);
