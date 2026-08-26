import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("intake lineage reconciliation contract", () => {
  it("preserva a reconciliação documental e os bloqueios de runtime, allowlist e produção", () => {
    const contract = readFileSync(resolve(root, "docs/gates/INTAKE_LINEAGE_RECONCILIATION_CONTRACT_001.md"), "utf8");
    const reconciliation = JSON.parse(readFileSync(resolve(root, "artifacts/catalogs/intake-lineage-reconciliation-v1.json"), "utf8"));
    const readinessIndex = JSON.parse(readFileSync(resolve(root, "artifacts/catalogs/rule-implementation-readiness-v1.json"), "utf8"));
    const ids = reconciliation.groups.flatMap((group: { rule_ids: string[] }) => group.rule_ids);
    const executableIds = new Set(readinessIndex.rules.filter((rule: { executable: boolean }) => rule.executable).map((rule: { rule_id: string }) => rule.rule_id));
    expect(reconciliation.scope).toEqual({ index: "rule-implementation-readiness-v1.json", executable_draft_count: 95, intake_required_count: 0 });
    expect(reconciliation.document_only).toBe(true);
    expect(reconciliation.runtime_change_prohibited).toBe(true);
    expect(reconciliation.allowlist_change_prohibited).toBe(true);
    expect(reconciliation.production_authorized).toBe(false);
    expect(reconciliation.groups.map((group: { group_id: string }) => group.group_id)).toEqual(["missing_intake_file", "legacy_intake_schema", "stale_intake_readiness"]);
    expect(ids).toHaveLength(34);
    expect(new Set(ids).size).toBe(34);
    expect(ids.every((id: string) => executableIds.has(id))).toBe(true);
    for (const group of reconciliation.groups) {
      expect(group.runtime_change_prohibited).toBe(true);
      expect(group.allowlist_change_prohibited).toBe(true);
      expect(group.production_authorized).toBe(false);
    }
    expect(contract).toContain("não pode modificar `DRAFT_RULE_AUTHORIZATIONS`");
    expect(contract).toContain("production_authorized=false");
    expect(contract).toContain("autorização explícita de Chris");
  });
});
