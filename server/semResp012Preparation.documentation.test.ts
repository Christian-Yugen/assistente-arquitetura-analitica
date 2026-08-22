import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/SEM-RESP-012.json");
const policyPath = resolve(projectRoot, "docs/rules/SEM_RESP_012_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(projectRoot, "docs/rules/SEM_RESP_012_LOGICAL_SPEC_PROPOSAL_001.md");

describe("SEM-RESP-012 — preparação governada", () => {
  it("preserva a proposta não executável, a privacidade e o bloqueio até autorização específica", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");

    expect(intake.rule.rule_id).toBe("SEM-RESP-012");
    expect(intake.local_readiness).toBe("intake_required");
    expect(intake.authorization.implementation_authorized).toBe(false);
    expect(intake.execution_blocked).toBe(true);
    expect(intake.missing_before_execution).toContain("authorization_gate");

    expect(policy).toContain("Esta é uma proposta **não executável**");
    expect(policy).toContain("exatamente `responsavel`");
    expect(policy).toContain("`responsible_candidate`");
    expect(policy).toContain("não identificará pessoas, áreas, equipes, cargos");
    expect(policy).toContain("A produção permanece bloqueada.");

    expect(specification).toContain("Especificação não executável.");
    expect(specification).toContain("SemanticResponsibleProfile(");
    expect(specification).toContain("confidence = 0.70");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');
  });
});
