import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/SEM-CAT-010.json");
const policyPath = resolve(projectRoot, "docs/rules/SEM_CAT_010_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(projectRoot, "docs/rules/SEM_CAT_010_LOGICAL_SPEC_PROPOSAL_001.md");

describe("SEM-CAT-010 — preparação governada", () => {
  it("mantém o intake, a proposta e a especificação bloqueados antes de qualquer implementação", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");

    expect(intake.rule.rule_id).toBe("SEM-CAT-010");
    expect(intake.local_readiness).toBe("intake_required");
    expect(intake.authorization.implementation_authorized).toBe(false);
    expect(intake.execution_blocked).toBe(true);
    expect(intake.missing_before_execution).toContain("authorization_gate");

    expect(policy).toContain("Esta é uma proposta **não executável**");
    expect(policy).toContain("exatamente `categoria`");
    expect(policy).toContain("`category_candidate`");
    expect(policy).toContain("A produção permanece bloqueada.");

    expect(specification).toContain("Especificação não executável.");
    expect(specification).toContain("SemanticCategoryProfile(");
    expect(specification).toContain("confidence = 0.70");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');
  });
});
