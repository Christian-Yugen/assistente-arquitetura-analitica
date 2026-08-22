import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/GRN-EXPL-002.json");
const policyPath = resolve(projectRoot, "docs/rules/GRN_EXPL_002_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(projectRoot, "docs/rules/GRN_EXPL_002_LOGICAL_SPEC_PROPOSAL_001.md");
const calibrationGatePath = resolve(projectRoot, "docs/gates/GRN_EXPL_002_DRAFT_CALIBRATION_001.md");

describe("GRN-EXPL-002 — ativação governada", () => {
  it("preserva a ativação exclusiva em draft, a calibração e o bloqueio produtivo", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");
    const calibrationGate = readFileSync(calibrationGatePath, "utf8");

    expect(intake.rule.rule_id).toBe("GRN-EXPL-002");
    expect(intake.rule.scope).toBe("sheet");
    expect(intake.local_readiness).toBe("executable_draft");
    expect(intake.status).toBe("executable_draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.authorization.required_gate).toBe("GRN-EXPL-002-RECONSTRUCTION-AUTHORIZATION-001");
    expect(intake.execution_blocked).toBe(false);
    expect(intake.missing_before_execution).toEqual([]);

    expect(policy).toContain("exatamente `id`, `chave` ou `key`");
    expect(policy).toContain("`explicit_key_candidate`");
    expect(policy).toContain("não declara chave primária");
    expect(policy).toContain("A produção permanece bloqueada.");

    expect(specification).toContain("ExplicitKeySheetProfile(");
    expect(specification).toContain("eligible_candidate_count == 1");
    expect(specification).toContain("não identifica a coluna");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');

    expect(calibrationGate).toContain("GD-GRN-EXPL-002-001");
    expect(calibrationGate).toContain("ab368d7e0758c07ea0afd6974b5ac6c9335354c2346e1ab9bde27be546fc6b7a");
    expect(calibrationGate).toContain('`{"true_positives": 3, "false_positives": 0, "false_negatives": 0}`');
    expect(calibrationGate).toContain("Produção permanece bloqueada.");
  });
});
