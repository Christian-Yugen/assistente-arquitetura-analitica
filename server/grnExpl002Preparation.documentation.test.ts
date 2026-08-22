import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/GRN-EXPL-002.json");
const policyPath = resolve(projectRoot, "docs/rules/GRN_EXPL_002_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(projectRoot, "docs/rules/GRN_EXPL_002_LOGICAL_SPEC_PROPOSAL_001.md");

describe("GRN-EXPL-002 — preparação governada", () => {
  it("preserva a proposta não executável e bloqueia a execução até autorização específica", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");

    expect(intake.rule.rule_id).toBe("GRN-EXPL-002");
    expect(intake.rule.scope).toBe("sheet");
    expect(intake.local_readiness).toBe("intake_required");
    expect(intake.authorization.implementation_authorized).toBe(false);
    expect(intake.authorization.required_gate).toBe("GRN-EXPL-002-RECONSTRUCTION-AUTHORIZATION");
    expect(intake.execution_blocked).toBe(true);
    expect(intake.missing_before_execution).toContain("authorization_gate");

    expect(policy).toContain("Esta é uma proposta **não executável**");
    expect(policy).toContain("exatamente `id`, `chave` ou `key`");
    expect(policy).toContain("`explicit_key_candidate`");
    expect(policy).toContain("não declara chave primária");
    expect(policy).toContain("A produção permanece bloqueada.");

    expect(specification).toContain("ExplicitKeySheetProfile(");
    expect(specification).toContain("eligible_candidate_count == 1");
    expect(specification).toContain("não identifica a coluna");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');
  });
});
