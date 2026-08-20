import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

type RulesetArtifact = {
  ruleset_id: string;
  ruleset_version: string;
  status: string;
  diagnosis_contract_version: string;
  context_contract_version: string;
  category_counts: { quality: number };
  execution_order: string[];
  rule_files: string[];
  integration_controls: { production_ready: boolean; required_next_gates: string[] };
};

function readJson<T>(relativePath: string): T {
  const absolutePath = resolve(process.cwd(), relativePath);
  return JSON.parse(readFileSync(absolutePath, "utf8")) as T;
}

describe("quality ruleset 0.7.0 draft", () => {
  it("adds QLT-NUMTEXT-007 without promoting the quality ruleset to production", () => {
    const ruleset = readJson<RulesetArtifact>("artifacts/rulesets/quality-ruleset-v0.7.0.json");

    expect(ruleset).toMatchObject({
      ruleset_id: "PM-MVP-PBI-RULESET-QUALITY-007",
      ruleset_version: "0.7.0-draft",
      status: "draft",
      diagnosis_contract_version: "1.0.0",
      context_contract_version: "1.6.0",
      category_counts: { quality: 7 },
      integration_controls: { production_ready: false },
    });
    expect(ruleset.execution_order.at(-1)).toBe("QLT-NUMTEXT-007");
    expect(ruleset.rule_files).toContain("artifacts/rules/QLT-NUMTEXT-007/qlt_numtext_007.json");
    expect(ruleset.integration_controls.required_next_gates).toEqual([
      "G7.3-isolated-implementation",
      "G7.4-ruleset-integration",
      "G7.5-documentary-closure",
    ]);
  });

  it("requires compatible dependencies and aggregate-only evidence for QLT-NUMTEXT-007", () => {
    const rule = readJson<{
      rule_id: string;
      diagnosis_contract_version: string;
      status: string;
      dependencies: { executes_after_rule_ids: string[]; requires_context_paths: string[] };
      privacy: { raw_values_in_findings: boolean; allowed_evidence: string[] };
    }>("artifacts/rules/QLT-NUMTEXT-007/qlt_numtext_007.json");

    expect(rule).toMatchObject({
      rule_id: "QLT-NUMTEXT-007",
      diagnosis_contract_version: "1.0.0",
      status: "draft",
      privacy: { raw_values_in_findings: false },
    });
    expect(rule.dependencies.executes_after_rule_ids).toEqual([
      "QLT-NULL-001",
      "QLT-EMPTYCOL-003",
      "QLT-MIXTYPE-005",
    ]);
    expect(rule.dependencies.requires_context_paths).toContain("column.profile.numeric_text_candidate_ratio");
    expect(rule.privacy.allowed_evidence).toEqual(["counts", "ratios", "basis", "column_name"]);
  });

  it("keeps the integration gates pending after isolated implementation", () => {
    const ruleset = readJson<RulesetArtifact>("artifacts/rulesets/quality-ruleset-v0.7.0.json");

    expect(ruleset.status).toBe("draft");
    expect(ruleset.integration_controls.production_ready).toBe(false);
    expect(ruleset.integration_controls.required_next_gates).toContain("G7.4-ruleset-integration");
  });
});
